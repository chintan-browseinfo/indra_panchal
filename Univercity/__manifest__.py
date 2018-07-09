{
	'name':'univercity',
	'version':'1.0',
	'category':'Sales',
	'sequence':120,
	'summary':'UniverCity Module',
	'description':"""Online admission unvercity portal
	""",
	'website':'https://www.browseinfo,in',
	'depends':['sale','mail'],
	'data':[
		'views/student_inquiry_details_views.xml',
		'views/student_application_details_views.xml', 
		'views/univercity_club_views.xml',
		'views/education_stream_views.xml',
		'views/univercity_courses_views.xml',
		'views/qualification_rules_views.xml',
		],
	'demo':[],
	'css':[],
	'installable': True,
	'auto_install': False,
	'application': False,
}