"""Package only the public download page and the verified, signed Android APK."""
import hashlib
import argparse
import json
from datetime import datetime
from pathlib import Path
import shutil
import stat
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

repo = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--apk', type=Path, required=True)
parser.add_argument('--verification', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
apk = args.apk.resolve()
report = json.loads(args.verification.read_text())
version = report['version']; build = report['versionCode']
assert version == '0.3.3' and isinstance(build, int) and build >= 15
apk_name = f'Quizfolk-Android-{version}-{build}.apk'
assert hashlib.sha256(apk.read_bytes()).hexdigest() == report['apkSHA256']
assert report['signed'] and report['fcmClientConfigured']
stage_home = args.output.resolve() / f'quizfolk-download-{build}'
stage = stage_home / 'public_html/quizfolk-download'
stage.mkdir(parents=True, exist_ok=True)
files = {
    'index.html': repo / 'web-download/index.html',
    '.htaccess': repo / 'web-download/.htaccess',
    'download.php': repo / 'web-download/download.php',
    'stats.php': repo / 'web-download/stats.php',
    'stats.js': repo / 'web-download/stats.js',
    'stats.css': repo / 'web-download/stats.css',
    'logo.png': repo / 'iOS/Assets.xcassets/AppIcon.appiconset/AppIcon.png',
    'nunito.ttf': repo / 'android/app/src/main/res/font/nunito.ttf',
    'font-license.txt': repo / 'android/FONT-LICENSE.txt',
    apk_name: apk,
}
for name, source in files.items():
    shutil.copyfile(source, stage / name)
for name in ['index.html', 'download.php', '.htaccess']:
    path = stage / name
    text = path.read_text(encoding='utf-8').replace('Quizfolk-Android-0.3.3-15.apk', apk_name)
    text = text.replace('Version 0.3.3 (15) · 3.8 MB', f'Version {version} ({build}) · {apk.stat().st_size / 1048576:.1f} MB')
    text = text.replace('21,667</strong>', f'{report["questions"]:,}</strong>').replace('30 topics</strong>', f'{report["categories"]} topics</strong>')
    text = text.replace('(11|12|13|14|15)', '(' + '|'.join(str(n) for n in range(11,build+1)) + ')')
    path.write_text(text, encoding='utf-8')
(stage / 'SHA256SUMS.txt').write_text(report['apkSHA256'] + '  ' + apk_name + '\n')
archive = args.output.resolve() / f'Quizfolk-Android-download-page-{version}-{build}.zip'
helper = stage_home / 'quizfolk-service/download-tracking/metrics.php'
helper.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(repo / 'web-download/server/metrics.php', helper)
helper.write_text(helper.read_text(encoding='utf-8').replace('Quizfolk-Android-0.3.3-15.apk',apk_name).replace('0.3.3 (15)',f'{version} ({build})'),encoding='utf-8')
with ZipFile(archive, 'w', ZIP_DEFLATED) as z:
    targets = [('public_html/quizfolk-download/' + name, stage / name) for name in [*files, 'SHA256SUMS.txt']]
    targets.append(('quizfolk-service/download-tracking/metrics.php', helper))
    for target, source in targets:
        item = ZipInfo(target, date_time=datetime.now().timetuple()[:6])
        item.create_system = 3
        item.external_attr = (stat.S_IFREG | 0o644) << 16
        item.compress_type = ZIP_DEFLATED
        z.writestr(item, source.read_bytes())
print(json.dumps({'archive': str(archive), 'preview': str(stage), 'apkSHA256': report['apkSHA256'], 'files': len(targets)}))
