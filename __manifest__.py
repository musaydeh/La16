{
    'name': "BoM Structure Price and Cost",
    'summary': "Add price and cost information to BoM structure",
    'description': """
        Extends BoM structure with additional price and cost information
    """,
    'author': "Osama Ramadan",
    'category': 'Manufacturing/Manufacturing',
    'version': '18.0.0.1',
    'depends': ['mrp_account'],
    'data': [
        'data/ir_cron.xml',
        'report/mrp_report_bom_structure.xml',
        'views/views.xml',
        'views/bom_view.xml',
        'views/product_category_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'boM_ctructure_price_cost/static/src/**/*.js',
            'boM_ctructure_price_cost/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
}
