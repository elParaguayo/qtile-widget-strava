pkgname=python-stravalib-git
_pkgname=stravalib
pkgver=388.e9a7c32
pkgrel=1
provides=("$_pkgname")
conflicts=("$_pkgname")
pkgdesc="Library to provide simple client interface to Strava's REST API (v3)."
url="https://github.com/hozn/$_pkgname"
arch=("any")
license=("APACHE2")
depends=("python>=3" "python-requests" "python-pytz" "python-arrow" "python-six")
source=("git+https://github.com/hozn/$_pkgname.git")
md5sums=("SKIP")

pkgver()
{
  cd "$_pkgname"
  echo $(git rev-list --count HEAD).$(git rev-parse --short HEAD)
}

package()
{
  cd "$_pkgname"
  python setup.py install --root="$pkgdir"
}
