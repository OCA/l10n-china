import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo9-addons-oca-l10n-china",
    description="Meta package for oca-l10n-china Odoo addons",
    version=version,
    install_requires=[
        'odoo9-addon-l10n_cn_hr_payroll',
        'odoo9-addon-l10n_cn_partner',
        'odoo9-addon-website_certificate',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 9.0',
    ]
)
