import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo10-addons-oca-l10n-china",
    description="Meta package for oca-l10n-china Odoo addons",
    version=version,
    install_requires=[
        'odoo10-addon-l10n_cn_hr_payroll',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 10.0',
    ]
)
