#!/usr/bin/env python3
"""Isolated real-browser QA for a generated architecture reader.

Run explicitly with --reader review.html --output browser-checks.json. A browser
launch block is recorded as blocked, never as a passing or skipped interaction
test. No existing browser profile or signed-in session is used.
"""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading


def run(reader, output, chromium='/usr/bin/chromium', screenshots=None):
    from playwright.sync_api import sync_playwright
    reader, output = Path(reader).resolve(), Path(output)
    result = {'profile': 'architecture-reader-browser-v1', 'status': 'not-run', 'checks': [], 'errors': [],
              'reader': str(reader), 'browser': chromium}
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(reader.parent)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/'
    url = base + reader.name
    try:
        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch(executable_path=chromium, headless=True)
            except Exception as error:
                result.update(status='blocked', stage='browser-launch', error=str(error))
                return result
            try:
                context = browser.new_context(viewport={'width':1440, 'height':960}, device_scale_factor=1)
                page = context.new_page()
                page.on('pageerror', lambda e: result['errors'].append(str(e)))
                external = []
                def route(request):
                    if request.request.url.startswith(base):
                        request.continue_()
                    else:
                        external.append(request.request.url)
                        request.abort()
                page.route('**/*', route)
                page.goto(url)
                page.wait_for_selector('.thread-card')
                data = page.locator('#reader-data').text_content()
                payload = json.loads(data)
                thread_count = len({s.get('slice',s['id']) for s in payload['architecture'].get('scenarios',[])})
                assert page.locator('.thread-card').count() == thread_count
                assert page.locator('.architecture-svg').count() == 0
                result['checks'].append('Overview exposes thread choices without stacking diagrams or evidence rows')
                if screenshots:
                    Path(screenshots).mkdir(parents=True, exist_ok=True)
                    page.screenshot(path=str(Path(screenshots)/'overview.png'), full_page=True)
                for section in ['operational','functions','logical','scenarios','requirements','decisions','evidence']:
                    page.locator(f'#navigation a[data-section="{section}"]').click()
                    page.wait_for_function('(section) => location.hash.startsWith("#"+section)',arg=section)
                    page.locator(f'#navigation a[data-section="{section}"][aria-current="page"]').wait_for()
                    assert page.locator('h1').inner_text()
                result['checks'].append('Every top-level navigation destination renders')
                page.goto(url+'#functions')
                page.wait_for_selector('.architecture-svg')
                old = page.locator('.architecture-svg').get_attribute('data-view-id')
                page.locator('[data-mode="decomposition"]').click()
                page.wait_for_function('(old) => document.querySelector(".architecture-svg").getAttribute("data-view-id")!==old',arg=old)
                node = page.locator('.architecture-svg [data-mark-kind="node"]').first
                node.focus();page.keyboard.press('Enter')
                assert page.locator('#inspector').is_visible()
                assert page.locator('#inspector-heading').inner_text()
                page.keyboard.press('Escape')
                assert page.locator('#inspector').is_hidden()
                assert node.evaluate('(e) => document.activeElement === e')
                node.press('Enter')
                page.get_by_role('button', name='Close inspector').click()
                assert page.locator('#inspector').is_hidden()
                assert node.evaluate('(e) => document.activeElement === e')
                result['checks'].append('Question selection changes projection; keyboard inspection restores focus after Escape and Close')
                for scenario in payload['architecture'].get('scenarios',[]):
                    for group in scenario.get('parallelGroups',[]):
                        page.goto(url+'#scenarios?mode=scenario&scope='+scenario['id'])
                        page.wait_for_selector('.concurrency-callout')
                        for control in ['fork','join']:
                            identity=scenario['id']+'/'+group['id']+'/'+control
                            assert page.locator(f'[data-record-id="{identity}"]').count()==1
                result['checks'].append('Explicit concurrency groups expose separate fork and join controls')
                if payload.get('evidence'):
                    page.goto(url+'#evidence');page.wait_for_selector('#table-query')
                    page.locator('#table-query').fill(payload['evidence'][0]['id'])
                    assert page.locator('.data-table tbody tr').count()>=1
                    assert page.locator('.data-table tbody tr').count()<=25
                    result['checks'].append('Retained source inventory search is paginated and selectable')
                page.goto(url+'#overview');page.wait_for_selector('.thread-card')
                page.keyboard.press('/')
                assert page.locator('#global-search').evaluate('(e)=>e===document.activeElement')
                page.locator('#global-search').fill(payload['architecture']['functions'][0]['id'])
                page.wait_for_selector('#search-results button')
                page.keyboard.press('Enter');assert page.locator('#inspector').is_visible()
                result['checks'].append('Global keyboard search selects an architecture record')
                page.keyboard.press('Escape')
                assert page.locator('#global-search').evaluate('(e) => document.activeElement === e')
                page.set_viewport_size({'width':390,'height':844})
                page.goto(url+'#overview');page.wait_for_selector('.thread-card')
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                if screenshots:
                    page.screenshot(path=str(Path(screenshots)/'mobile-overview.png'),full_page=True)
                result['checks'].append('Mobile overview has no body-level horizontal overflow')
                assert not external, 'Unexpected external requests: '+repr(external)
                assert not result['errors'], repr(result['errors'])
                result['checks'].append('No page runtime errors or external network dependency')
                result['status']='passed'
            finally:
                browser.close()
    except Exception as error:
        result.update(status='failed',error=str(error))
    finally:
        server.shutdown();server.server_close()
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reader',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--chromium',default='/usr/bin/chromium')
    parser.add_argument('--screenshots',type=Path)
    args=parser.parse_args()
    result=run(args.reader,args.output,args.chromium,args.screenshots)
    print(json.dumps({'status':result['status'],'checks':len(result['checks']),'output':str(args.output)}))
    raise SystemExit(0 if result['status']=='passed' else 2)
