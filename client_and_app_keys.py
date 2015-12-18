from keen.client import KeenClient

# API Keys for EnhatchMarketingApp2.0
client = KeenClient(
    project_id=open("project_id.txt", 'r').read(),
    master_key=open("master_key.txt", 'r').read(),
    write_key=open("write_key.txt", 'r').read(),
    read_key=open("read_key.txt", 'r').read()
)

account_app_keys = {'enhatch': '118368274437335737698029276469999809095',
                    'rr donnelly': '122169787206987846341383818731152558295',
                    'enhatch test': '129690986843314177890874392835790686791',
                    'ge transportation': '161299849888704839492897537232844536620',
                    'sonoma': '181479502579786137791904991511865109911',
                    'matt app': '187164587218548182461213257669257342645',
                    'paradigm spine': '224234185580937634736656715550056596303',
                    'allied building products': '253836980674808659119433391188831533066',
                    'ge ms&d': '285481600560299472311537967916336092115',
                    'medicrea': '28957996790114179931087019134108290920',
                    'seaspine': '293004830260428685669112292533809804613',
                    'centinel spine': '31544617854315997232220268879565974600',
                    'echo': '35431404049861511531147680883494651221',
                    'fh ortho': '71458724716185243148256933560969741161',
                    'wartsila': '95877466981632317159181119372243691526'}