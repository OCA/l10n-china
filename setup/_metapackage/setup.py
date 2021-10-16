import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-oca-l10n-china",
    description="Meta package for oca-l10n-china Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-l10n_cn_fapiao',
        'odoo8-addon-payment_alipay',
        'odoo8-addon-payment_wcpay',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 8.0',
    ]
)
