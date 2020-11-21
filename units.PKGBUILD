pkgname=python-units
_name=units
pkgver=0.07
pkgrel=1
pkgdesc="Python support for quantities with units."
arch=('any')
url="https://pypi.org/project/units/"
license=('Apache')
makedepends=('python-setuptools')
source=('https://files.pythonhosted.org/packages/33/8c/76112215f71aad89ffecae90dd1e0a681ad8f750df994d4ce1275bca50a2/units-0.07.tar.gz')
sha256sums=('43eb3e073e1b11289df7b1c3f184b5b917ccad178b717b03933298716f200e14')


package() {
  cd $_name-$pkgver
  python setup.py install --root="$pkgdir/"
}
