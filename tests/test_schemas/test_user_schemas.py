import uuid
import pytest
from pydantic import ValidationError, HttpUrl
from datetime import datetime
from app.schemas.user_schemas import ErrorResponse, ProfessionalStatus, UserBase, UserCreate, UserUpdate, UserResponse, UserListResponse, LoginRequest
from app.schemas.link_schema import Link

# Fixtures for common test data
@pytest.fixture
def user_base_data():
    return {
        "nickname": "john_doe_123",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "AUTHENTICATED",
        "bio": "I am a software engineer with over 5 years of experience.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg",
        "linkedin_profile_url": "https://linkedin.com/in/johndoe",
        "github_profile_url": "https://github.com/johndoe"
    }

@pytest.fixture
def user_create_data(user_base_data):
    return {**user_base_data, "password": "SecurePassword123!"}

@pytest.fixture
def user_update_data():
    return {
        "email": "john.doe.new@example.com",
        "nickname": "j_doe",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "I specialize in backend development with Python and Node.js.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe_updated.jpg"
    }

@pytest.fixture
def user_response_data(user_base_data):
    return {
        "id": uuid.uuid4(),
        "nickname": user_base_data["nickname"],
        "first_name": user_base_data["first_name"],
        "last_name": user_base_data["last_name"],
        "role": user_base_data["role"],
        "email": user_base_data["email"],
        # "last_login_at": datetime.now(),
        # "created_at": datetime.now(),
        # "updated_at": datetime.now(),
        "links": []
    }

@pytest.fixture
def login_request_data():
    return {"email": "john_doe_123@emai.com", "password": "SecurePassword123!"}

# Tests for UserBase
def test_user_base_valid(user_base_data):
    user = UserBase(**user_base_data)
    assert user.nickname == user_base_data["nickname"]
    assert user.email == user_base_data["email"]

# Tests for UserCreate
def test_user_create_valid(user_create_data):
    user = UserCreate(**user_create_data)
    assert user.nickname == user_create_data["nickname"]
    assert user.password == user_create_data["password"]

# Tests for UserUpdate
def test_user_update_valid(user_update_data):
    user_update = UserUpdate(**user_update_data)
    assert user_update.email == user_update_data["email"]
    assert user_update.first_name == user_update_data["first_name"]

# Tests for UserResponse
def test_user_response_valid(user_response_data):
    user = UserResponse(**user_response_data)
    assert user.id == user_response_data["id"]
    # assert user.last_login_at == user_response_data["last_login_at"]

# Tests for LoginRequest
def test_login_request_valid(login_request_data):
    login = LoginRequest(**login_request_data)
    assert login.email == login_request_data["email"]
    assert login.password == login_request_data["password"]

# Parametrized tests for nickname and email validation
@pytest.mark.parametrize("nickname", ["test_user", "test-user", "testuser123", "123test"])
def test_user_base_nickname_valid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    user = UserBase(**user_base_data)
    assert user.nickname == nickname

@pytest.mark.parametrize("nickname", ["test user", "test?user", "", "us"])
def test_user_base_nickname_invalid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Parametrized tests for URL validation
@pytest.mark.parametrize("url", ["http://valid.com/profile.jpg", "https://valid.com/profile.png", None])
def test_user_base_url_valid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    user = UserBase(**user_base_data)
    assert user.profile_picture_url == url

@pytest.mark.parametrize("url", ["ftp://invalid.com/profile.jpg", "http//invalid", "https//invalid"])
def test_user_base_url_invalid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Test for ProfessionalStatus
def test_professional_status_valid():
    status = ProfessionalStatus(is_professional=True)
    assert status.is_professional == True

# Test for ErrorResponse
def test_error_response_valid():
    error = ErrorResponse(error="Not Found", details="The requested resource was not found.")
    assert error.error == "Not Found"
    assert error.details == "The requested resource was not found."

# Test for UserListResponse
def test_user_list_response_valid(user_response_data):
    user_list = UserListResponse(items=[user_response_data]*10, total=100, page=1, size=10)
    assert len(user_list.items) == 10
    assert user_list.total == 100
    assert user_list.page == 1
    assert user_list.size == 10

# Parametrized tests for role validation in UserBase
@pytest.mark.parametrize("role", ["invalid_role", "", None])
def test_user_base_role_invalid(role, user_base_data):
    user_base_data["role"] = role
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Fixtures for common test data
@pytest.fixture
def link_data():
    return {
        "rel": "self",
        "href": "https://api.example.com/qr/123",
        "action": "GET",
        "type": "application/json"
    }

# Tests for Link
def test_link_valid(link_data):
    link = Link(**link_data)
    assert link.rel == link_data["rel"]
    assert link.href == link_data["href"]
    assert link.action == link_data["action"]
    assert link.type == link_data["type"]

# Parametrized tests for rel, action and type validation
@pytest.mark.parametrize("field", ["rel", "action", "type"])
def test_link_field_invalid(field, link_data):
    link_data[field] = ""  # empty string is invalid
    with pytest.raises(ValidationError):
        Link(**link_data)

# Parametrized tests for href (HttpUrl) validation
@pytest.mark.parametrize("url", ["http://valid.com", "https://valid.com", None])
def test_link_href_valid(url, link_data):
    link_data["href"] = url
    link = Link(**link_data)
    assert str(link.href) == url

@pytest.mark.parametrize("url", ["ftp://invalid.com", "http//invalid", "https//invalid"])
def test_link_href_invalid(url, link_data):
    link_data["href"] = url
    with pytest.raises(ValidationError):
        str(Link(**link_data))
