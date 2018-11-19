

from falchy.core import auth
from falchy.db import sql
import falcon 

class CoreMiddleWare:
    def __init__(self,db_engine):
        self.db_engine = db_engine

   
    def process_request(self,req,resp):
        conn = self.db_engine.connect()
        
        req.context['db'] = sql.Db(connection = conn)


    def process_resource(self,req,resp,resource,params):
        req.context['transaction'] = req.context['db']._connection.begin()


    def process_response(self,req,resp,resource,req_succeeded):
        try:
            if req_succeeded:
                req.context['transaction'].commit()
            else:
                req.context['transaction'].rollback()
        except:
            pass
        
        req.context['db']._connection.close()


 

class CORSMiddleWare:
    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('Access-Control-Allow-Origin','*')
        if (req_succeeded and req.method == 'OPTIONS' and req.get_header('Access-Control-Request-Method')):
            #preflight CORS request

            allow = resp.get_header('Allow')
            resp.delete_header('Allow')

            allow_headers = req.get_header(
                'Access-Control-Request-Headers', default='*'
            )

            resp.set_headers((
                ('Access-Control-Allow-Methods', allow),
                ('Access-Control-Allow-Headers', allow_headers),
                ('Access-Control-Max-Age', '86400'),  # 24 hours
            ))




class AuthMiddleWare:

    def __init__(self, secret_key):
        self.secret_key = secret_key
    
    def get_db(self, req):
        return req.context['db']
        
    def process_resource(self,req,resp,resource,params):
        

        if req.method != 'OPTIONS':
            
            must_login = True
            auth_token_type = 'Bearer'

            try:
                must_login = resource.login_required #we expect login_required = False
            except AttributeError:
                pass
            
            try:
                auth_token_type = resource.auth_token_type #we expect login_required = False
            except AttributeError:
                pass
                

            if must_login:
                auth_data = None

                if auth_token_type == 'Bearer':
                    secret_key = self.get_secret_key(req)

                    auth_data = auth.validate_bearer_token( bearer_token = req.auth , secret_key = secret_key )
                    
                if auth_data is None:
                    raise falcon.HTTPUnauthorized(description = 'Login Required')
                
                req.context['auth'] = auth_data
             
    def get_secret_key(self,req):
        return self.secret_key

            


class MultitenantMiddleWare:
    """ this injects tenant_id and / or organization_id to the resources. For those authenticated 
    It injects only if the values are not provided
    
    """

    def process_resource(self,req,resp,resource,params):
        resource.multitenant = False
        if req.method != 'OPTIONS':
            
            try:
                auth = req.context['auth']
            except KeyError:
                return None
            
            #set organization id. check first if exists so as not to override

            try:
                organization_id = params['organization_id']
                print ("Exists organization_id")
            except KeyError:
                params['organization_id'] = auth.get("organization_id")
            
            try:
                tenant_id = params['tenant_id']
                print ("Exists tenant_id")
            except KeyError:
                params['tenant_id'] = auth.get("tenant_id")
            
            print ("ORG", params['organization_id'])
            print ("Tenant",  params['tenant_id'])

    

