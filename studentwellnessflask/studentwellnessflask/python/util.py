#studentwellnessflask/flask/util.py
from flask_assets import Bundle, Enviorment
from . import app
bundles = {
	'index_js': Bundle(
		'js/lib/jquery-3.4.1.js'
	),

	'index_img': Bundle(
		'Images/CCSULogo.svg'
	),

	'index_css': Bundle(
		'css/lib/bootstrap.css'
		'css/SignIn.css'
	),

	'reg_js': Bundle(
		'js/lib/jquery-3.4.1.js'
	),

	'reg_img': Bundle(
		'Images/CCSULogo.svg'
	),

	'reg_css': Bundle(
		'css/lib/bootstrap.css'
		'css/RegistrationCSS.css'
	),

	'resetpass_js': Bundle(
		'js/lib/jquery-3.4.1.js'
	),

	'resetpass_img': Bundle(
		'Images/CCSULogo.svg'
	),

	'resetpass_css': Bundle(
		'css/lib/bootstrap.css'
		'css/ResetPass.css'
	)
}
assets = Enviorment(app)
assets.register(bundles)
index_js.build()
index_css.build()
index_img.build()
reg_js.build()
reg_css.build()
reg_img.build()
resetpass_js.build()
resetpass_css.build()
resetpass_img.build()
