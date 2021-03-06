# coding:utf-8
import urllib
import md5
from openstack.middleware.common.common import send_request,plog, IP_keystone, PORT_keystone
from openstack.middleware.common.urls import url_user_common, url_user_action,url_user_project,url_project_member,url_project_user_action,url_project_user_del, \
    url_project_list
from openstack.middleware.login.login import get_admin_project_id,get_admin_token
from openstack.middleware.common.common_api import CommonApi
class User(object):
    def __init__(self):
        self.password = md5.md5("baifendian").hexdigest()
        self.domain_id = ""
        self.role_id = ""

    @plog("User._get_domain")
    def _get_domian(self):
        if not self.domain_id:
            self.domain_id = CommonApi.get_domain_id({"name":"default"})["domains"][0]["id"]

    @plog("User._get_role")
    def _get_role(self):
        if not self.role_id:
            self.role_id = CommonApi.get_role_id({"name":"user"})["roles"][0]["id"]

    @plog("User.list")
    def list(self,query_dict=None):
        '''
        列出和查询用户
        :param query_dict:
        :return:
        '''
        admin_token = get_admin_token()
        assert admin_token != "","can not login with admin user"
        path = url_user_common
        method = "GET"
        head = {"Content-Type": "application/json", "X-Auth-Token": admin_token}
        params = ""
        if query_dict:
            query_str = urllib.urlencode(query_dict)
            path = "%s?%s" % (path, query_str)
        ret = send_request(method, IP_keystone, PORT_keystone, path, params, head)
        return ret

    @plog("User.list_pro")
    def list_pro(self,query_dict=None):
        '''
        列出所有project，由于都是keystone的接口，所以和user的放在一起
        :param query_dict:
        :return:
        '''
        admin_token = get_admin_token()
        assert admin_token != "","can not login with admin user"
        path = url_project_list
        method = "GET"
        head = {"Content-Type": "application/json", "X-Auth-Token": admin_token}
        params = ""
        if query_dict:
            query_str = urllib.urlencode(query_dict)
            path = "%s?%s" % (path, query_str)
        ret = send_request(method, IP_keystone, PORT_keystone, path, params, head)
        return ret

    @plog("User.create")
    def create(self,name,project_id=None,password=None):
        '''
        创建用户
        :param name:
        :param project_id:
        :param passward:
        :return:
        '''
        admin_token = get_admin_token()
        assert admin_token != "","can not login with admin user"
        self._get_domian()
        path = url_user_common
        method = "POST"
        head = {"Content-Type": "application/json", "X-Auth-Token": admin_token}
        params = {"user":{"name":name,"domain_id":self.domain_id,"enabled":True}}
        if project_id:
            params["user"].update({"default_project_id":project_id})
        if password:
            params["user"].update({"password":password})
        ret = send_request(method,IP_keystone,PORT_keystone,path,params,head)
        return ret

    @plog("User.get_id_by_name_user")
    def get_id_by_name(self,name):
        '''
        通过用户名获取用户id
        :param name:
        :return:
        '''
        tmp_dict = self.list({"name":name})
        assert tmp_dict != 1
        user_id = tmp_dict["users"][0].get("id","")
        return user_id

    @plog("User.get_id_by_name_pro")
    def get_id_by_name_pro(self,name):
        '''
        通过project名字获取project id
        :param name:
        :return:
        '''
        tmp_dict = self.list_pro({"name":name})
        assert tmp_dict != 1
        pro_id = tmp_dict["projects"][0].get("id","")
        return pro_id


    @plog("User.delete")
    def delete(self):
        pass

    @plog("User.update")
    def update(self):
        pass

    @plog("User.get_project")
    def get_user_project(self,name):
        '''
        获取指定user所在的project
        :param name:
        :return:
        '''
        admin_token = get_admin_token()
        assert admin_token != "","can not login with admin user"
        user_id = self.get_id_by_name(name)
        assert user_id != 1,"get user id faild"
        path = url_user_project.format(user_id=user_id)
        method = "GET"
        params = ""
        head = {"Content-Type": "application/json", "X-Auth-Token": admin_token}
        ret = send_request(method, IP_keystone, PORT_keystone, path, params, head)
        return ret

    plog("User.get_project_user")
    def get_project_user(self,project_id):
        '''
        获取指定project中的成员
        :return:返回结果中只有user的id，没有name
        '''
        admin_token = get_admin_token()
        assert admin_token != "","can not login with admin user"
        path = url_project_member
        self._get_role()
        query_dict = {"role.id":self.role_id,"scope.project.id":project_id,"include_subtree":True}
        query_str = urllib.urlencode(query_dict)
        path = "%s?%s" % (path, query_str)
        method = "GET"
        params = ""
        head = {"Content-Type": "application/json", "X-Auth-Token": admin_token}
        ret = send_request(method, IP_keystone, PORT_keystone, path, params, head)
        return ret

    plog("User.project_user_add")
    def project_user_add(self,project_id,user_id):
        '''
        将user加入project中
        :return:
        '''
        admin_token = get_admin_token()
        assert admin_token != "","can not login with admin user"
        self._get_role()
        path = url_project_user_action.format(project_id=project_id,user_id=user_id,role_id=self.role_id)
        method = "PUT"
        params = ""
        head = {"Content-Type": "application/json", "X-Auth-Token": admin_token}
        ret = send_request(method, IP_keystone, PORT_keystone, path, params, head)
        return ret

    plog("User.project_user_del")
    def project_user_del(self,project_id,user_id):
        '''
        将user从project中移除
        :return:
        '''
        admin_token = get_admin_token()
        assert admin_token != "","can not login with admin user"
        self._get_role()
        path = url_project_user_del.format(project_id=project_id,user_id=user_id,role_id=self.role_id)
        method = "DELETE"
        params = ""
        head = {"Content-Type": "application/json", "X-Auth-Token": admin_token}
        ret = send_request(method, IP_keystone, PORT_keystone, path, params, head)
        return ret

    @plog("User.user_attach")
    def user_attach(self,project_name,user_add_list=None,user_del_list=None):
        '''
        1.判断新增用户是否存在，不存在则创建用户
        2.将新增用户加入project中(不需要判断是否已存在于project中)
        3.判断需要剔除的用户是否存在于project中，存在则剔除(不能直接剔除，否则会报错)
        :return:
        '''
        ret = 0
        user_list_tmp = self.list().get("users",[])
        user_list = {}
        map(lambda i:user_list.update({i["name"]:i["id"]}),user_list_tmp)
        project_id = self.get_id_by_name_pro(project_name)
        if user_add_list:
            for user in user_add_list:
                if user and user not in user_list: #防止user为空
                    ret_tmp = self.create(user,project_id,self.password)
                    assert ret_tmp != 1,'create user faild'
                    user_id = ret_tmp["user"].get("id","")
                else:
                    user_id = user_list[user]
                ret_tmp = self.project_user_add(project_id,user_id)
                assert ret_tmp != 1,"add user to project faild"
        if user_del_list:
            project_user_list_tmp = self.get_project_user(project_id)["role_assignments"]
            project_user_list = [i["user"]["id"] for i in project_user_list_tmp]
            for user in user_del_list:
                user_id = user_list.get(user,"")
                if user_id in project_user_list:
                    ret_tmp = self.project_user_del(project_id,user_id)
                    assert ret_tmp != 1,"del user from project faild"
        return ret
