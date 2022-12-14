**功能:登录**

请求数据格式:form-data

请求路径:api/user/login/

请求方式:POST

请求参数:



| 参数名   | 必填 | 字段类型 | 描述   |
| -------- | ---- | :------- | ------ |
| username | 是   | String   | 用户名 |
| password | 是   | String   | 密码   |





响应结果:返回的是数量

Json 

```
{
    "code": 200,
    "message": "ok",
    "info":{
    	"user_id":'用户id',
    	"username":'用户名',
    	'last_login':'最后登录时间',
    	'create_login':'创建时间',
    }
}
```





**功能:用户列表展示**

请求数据格式:form-data

请求路径:api/user/login/

请求方式:GET

请求参数:

| 参数名 | 必填 | 字段类型 | 描述               |
| ------ | ---- | :------- | ------------------ |
| page   | 是   | int      | 当前页             |
| limit  | 是   | int      | 每页展示数据的数量 |
| status | 是   | Sting    | 当前用户的状态     |
| query  | 否   | String   | 用户查询关键字     |



响应结果:

Json 

```
{
    "code": 200,
    "message": "ok",
    "info":{
    	"user_id":'用户id',
    	"username":'用户名',
    	'password':'密码',
    	'last_login':'最后登录时间',
    	'create_login':'创建时间',
    	'role':'用户所属角色',
    	'status':'用户状态(是否禁用)'
    }
}
```





**功能:添加账号**

请求数据格式:form-data

请求路径:api/account/add/

请求方式:POST

请求参数:

| 参数名   | 必填 | 字段类型 | 描述   |
| -------- | ---- | :------- | ------ |
| username | 是   | String   | 用户名 |
| password | 是   | String   | 密码   |



响应结果:

Json 

```
{
    "code": 200,
    "message": "ok",
    "info":{
    	"user_id":'用户id',
    	"username":'用户名',
    	
    }
}
```





**功能:编辑账号**

请求数据格式:form-data

请求路径:api/account/edit/

请求方式:POST

请求参数:

| 参数名   | 必填 | 字段类型 | 描述   |
| -------- | ---- | :------- | ------ |
| username | 是   | String   | 用户名 |
| password | 是   | String   | 密码   |



响应结果:

Json 

```
{
    "code": 200,
    "message": "ok",
    "info":{
    	"user_id":'用户id',
    	"username":'用户名',
    	
    }
}
```

