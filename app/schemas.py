import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class CallPostAuthorizeRes:
    protected_data: Dict
    consent_user: str
    metadata: Dict


@dataclass
class GetUsersPageReq:
    page_token: Optional[str] = None


@dataclass
class IntGroupData:
    group_id: str
    group_name: str
    role: str
    type: str
    status: str
    delivery_settings: str


@dataclass(order=True)
class FileDTO:
    container_name: str
    file_name: str
    file_type: Optional[str] = None


@dataclass
class UserEmail:
    address: str
    primary: Optional[bool] = None


@dataclass
class UserName:
    givenName: str
    familyName: str
    fullName: str


@dataclass
class UserMailData:
    is_enabled: Optional[bool] = None
    emails_sent: Optional[int] = None
    spam_emails_received: Optional[int] = None
    emails_received: Optional[int] = None
    reason: Optional[str] = None


@dataclass
class UserRecord:
    org_id: str
    int_name: str
    user_id: str
    primary_email: str
    is_admin: bool
    admin_extra_info: Dict
    suspended: bool
    archived: bool
    org_unit_path: str
    is_enrolled_in_2_sv: bool
    is_enforced_in_2_sv: bool
    name: UserName
    emails: List[UserEmail]
    mail_data: UserMailData
    password_strength: Optional[str] = None
    password_length_compliance: Optional[str] = None
    record_creation_time: Optional[datetime.datetime] = None
    record_last_update_time: Optional[datetime.datetime] = None
    last_login_time: Optional[datetime.datetime] = None
    creation_time: Optional[datetime.datetime] = None
    last_mail_fetch: Optional[datetime.datetime] = None
    groups: List[str] = field(default_factory=list)
    recovery_email: Optional[str] = field(default=None)
    user_photo: Optional[FileDTO] = None
    int_groups: List[IntGroupData] = field(default_factory=list)
    extra_data: Dict = field(default_factory=dict)


@dataclass
class GetUsersPageRes:
    users: List[UserRecord]
    page_token: Optional[str] = None


@dataclass
class GetDevicesReq:
    org_id: str
    user: UserRecord


@dataclass
class DeviceRecord:
    org_id: str
    int_name: str
    device_id: str
    resource_id: str
    user_email: str
    name: str
    device_name: str
    os: str
    os_version: str
    device_type: str
    profile_type: str
    last_sync: datetime.datetime
    record_creation_time: Optional[datetime.datetime] = None
    record_last_update_time: Optional[datetime.datetime] = None
    extra_data: Dict = field(default_factory=dict)


@dataclass
class GetDevicesRes:
    devices: List[DeviceRecord]
    page_token: Optional[str] = None


@dataclass
class GetAppsReq:
    org_id: str
    user: UserRecord


@dataclass
class AppRecord:
    org_id: str
    int_name: str
    user_name: str
    user_id: str
    client_id: str
    display_text: str
    native_app: bool
    scopes: List[str]
    is_grant_app: bool
    record_creation_time: Optional[datetime.datetime] = None
    record_last_update_time: Optional[datetime.datetime] = None
    user_key: Optional[str] = None
    verified: Optional[bool] = None


@dataclass
class GetAppsRes:
    apps: List[AppRecord]
    page_token: Optional[str] = None
