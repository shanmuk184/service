from api.stores.group import Group, GroupType, CreateEmployeeRequestParams, MemberMapping
from api.stores.user import SupportedRoles, User, GroupMapping, UserStatus
from tornado.gen import *
from api.core.user import UserHelper
from api.core.group import GroupHelper
import uuid

class GroupModel(object):
    def __init__(self, **kwargs):
        if not kwargs.get('db'):
            raise ValueError('db should be present')
        if kwargs.get('user'):
            self._user = kwargs.get('user')
        self.db = kwargs.get('db')

        if self._user:
            self._gh = GroupHelper(**kwargs)
            self._uh = UserHelper(**kwargs)
        elif self.db:
            self._gh = GroupHelper(db=self.db)
            self._uh = UserHelper(db=self.db)

    @coroutine
    def create_group(self, groupDict, userId=None, type=None):
        if not userId:
            userId = self._user.UserId
        group = Group()
        group.Name = groupDict.get(Group.PropertyNames.Name)
        group.OwnerId = userId
        if type:
            group.Type = type
        membermappings = [self._gh.create_member_mapping(self._user.UserId, [SupportedRoles.Admin])]
        group.MemberMappings = membermappings
        group.set_value(group.PropertyNames.CreatedTimeStamp, datetime.datetime.now())
        group.set_value(group.PropertyNames.UpdatedTimeStamp, datetime.datetime.now())
        group_result = yield self._gh.create_group_for_user(group.datadict)
        group.Id = group_result.inserted_id
        memberGroupMapping = self._uh.create_group_mapping(group_result.inserted_id, [SupportedRoles.Admin])
        yield self._gh.insert_group_mapping_into_user(self._user.UserId, memberGroupMapping.datadict)
        raise Return(group)

    # Pharmaceutical distributor is a kind of group that don't have link to Pharmacy company only reverse link
    @coroutine
    def create_pharmaceutical_distributor(self, **kwargs):
        group = self.create_group(kwargs, self._user.UserId, GroupType.PharmaDistributor)
        raise Return(group)
    # Dummy team for employees
    @coroutine
    def create_employee_team(self, **kwargs):
        group = self.create_group(kwargs, self._user.UserId, GroupType.EmployeeTeam)
        raise Return(group)

    @coroutine
    def get_groups_for_user(self, userId):
        if not userId:
            userId = self._user.UserId
        try:
            (groups) = yield self._gh.get_groups_for_user(userId)
        except Exception as e:
            raise Return((False, str(e)))
        else:
            raise Return((True, groups))

    def create_invited_state_user(self, invitedDict):
        employee=User()
        employee.Name = invitedDict.get(CreateEmployeeRequestParams.Name)
        employee.PrimaryEmail = invitedDict.get(CreateEmployeeRequestParams.EmailId)
        employee.UserId = uuid.uuid4()
        employee.Status=UserStatus.Invited
        employee.EmailValidated=False
        employee.CreatedTimeStamp=datetime.datetime.now()
        employee.UpdatedTimeStamp=datetime.datetime.now()
        return employee


    @coroutine
    def create_employee(self, employeeDict, groupId):
        """
            Employee added by admin.
            This method takes input from admin and creates user profile and
            creates membermapping for corresponding group.
            employeeDict should contain
            name,
            designation
            emailid
            :return:
        """
        if not (employeeDict and  groupId):
            raise NotImplementedError()
        employee=self.create_invited_state_user(employeeDict)
        employee_result = yield self._uh.save_user(employee.datadict)

        if employee_result:
            employee_mapping = MemberMapping()
            employee_mapping.MemberId = employee.UserId
            employee_mapping.Designation = employeeDict.get(CreateEmployeeRequestParams.Designation)
            employee_mapping.Roles=[SupportedRoles.Member]
            employee_mapping.JoinedTimeStamp = datetime.datetime.now()
            employee_mapping.LastUpdatedTimeStamp = datetime.datetime.now()
            self._gh.insert_member_mapping_into_group(groupId, employee_mapping.datadict)







