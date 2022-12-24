import os

media_path = "./media"


def user_folder_exists(user_id: int):
	if not os.path.exists(f"{media_path}"):
		os.mkdir(f"{media_path}")
	return os.path.exists(f"{media_path}/{user_id}")


def create_user_folder_if_not_exists(user_id: int):
	if not user_folder_exists(user_id):
		print(f"os.mkdir(", f"{media_path}/{user_id}", ')')
		os.mkdir(f"{media_path}/{user_id}")



def category_exist(user_id: int, category: str):
	create_user_folder_if_not_exists(user_id)
	return os.path.exists(f"{media_path}/{user_id}/{category}")


def list_categories(user_id: int):
	create_user_folder_if_not_exists(user_id)
	return os.listdir(f"{media_path}/{user_id}")


def create_category(user_id: int, category: str):
	create_user_folder_if_not_exists(user_id)
	if not category_exist(user_id, category):
		os.mkdir(f"{media_path}/{user_id}/{category}", mode=0o777)
	else:
		pass


def delete_category(user_id: int, category: str):
	create_user_folder_if_not_exists(user_id)
	if category_exist(user_id, category):
		os.system(f"rm -rf {media_path}/{user_id}/{category}")
	else:
		pass