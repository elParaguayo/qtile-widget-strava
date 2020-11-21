pkgname=qtile-widget-strava-git
_pkgname=qtile-widget-strava
pkgver=0.0.1
pkgrel=1
provides=("$_pkgname")
conflicts=("$_pkgname")
pkgdesc="Qtile widget to display strava stats."
url="https://github.com/elparaguayo/qtile-widget-strava.git"
license=("MIT")
depends=("python" "qtile" "python-dateutil")
source=("git+https://github.com/elparaguayo/$_pkgname.git")
md5sums=("SKIP")

pkgver()
{
  cd "$_pkgname"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package()
{
  cd "$_pkgname"
  python setup.py install --root="$pkgdir"
}
