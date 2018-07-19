{
	'name':'product',
	'version':'1.0',
	'sequence':120,
	'summary':'Product Bundle',
	'description':"""Online admission unvercity portal
	""",
	'website':'https://www.browseinfo.in',
	'author' :'Indra Panchal',
	'depends' : ['sale','base','product'],
	'data':[
		'wizard/add_pack_views.xml',
		'views/sale_product_views.xml',
		'views/product_bundle_views.xml',
		],
	'demo':[],
	'css':[],
	'installable': True,
	'auto_install': False,
	'application': False,
}