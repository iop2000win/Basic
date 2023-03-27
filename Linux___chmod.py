'''
파이썬 코드를 통해 경로에 대한 권한을 변경하는 작업
user_id & group_id를 특정 값으로 입력해주기 위해서는,
pwd, grp 패키지를 이용해야 한다.

아닐 경우, str을 입력 값으로 받지 않는다.
'''

import os
import pwd # user_id 변경을 위한 패키지
import grp # group_id 변경을 위한 패키지

sample_path = os.getcwd()

user_id = pwd.getpwnam('sample_u_name').pw_uid
group_id = grp.getgrnam('sample_g_name').gr_gid

os.chown(sample_path, user_id, group_id)

os.chmod(sample_path, 0o770) # 맨 앞에 0o를 붙여 주어야 한다.
