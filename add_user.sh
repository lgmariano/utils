#!/bin/bash

# Creates a new user interactively

set_user()
{
	echo "User name:"
	read CMD_USER_NAME

	if [ "$CMD_USER_NAME" == "" ]; then
		return 1
	fi

	return 0
}

# home directory
set_home()
{
	echo -e "\nHome directory:"
	echo -e " -> blank for default: /home/$CMD_USER_NAME"
	echo -e " -> 'n' for no home"
	echo -e " -> specify home directory, ex: /opt/new_user"
	read HOME_DIR

	if [ "$HOME_DIR" == "" ]; then
		HOME_DIR="/home/$CMD_USER_NAME"
		CMD_HOME_DIR=""
	elif [ "$HOME_DIR" == "n" ]; then
		HOME_DIR=""
		CMD_HOME_DIR=" --no-create-home"		# no home directory
	else
		CMD_HOME_DIR=" --home $HOME_DIR"
	fi

	return 0
}

# shell
set_shell()
{
	echo "Use default login shell $SHELL: [Y/n]"
	read DEF_SHELL

	if [ "$DEF_SHELL" == "y" ] || [ "$DEF_SHELL" == "" ]; then
		DEF_SHELL=$(echo $SHELL)
		CMD_SHELL=""
	elif [ "$DEF_SHELL" == "n" ]; then
		echo "Choose one of the following shells:"
		cat /etc/shells
		read DEF_SHELL
		CMD_SHELL=" --shell $DEF_SHELL"
	else
		echo "Invalid option"
		return 1
	fi

	return 0
}

# expire date
set_expire_date()
{
	echo "Set expire date? [y/N]"
	read DATE

	if [ "$DATE" == "y" ]; then
		echo "Year:"
		read YEAR
		echo "Month"
		read MONTH
		echo "Day:"
		read DAY

		DATE="$DAY-$MONTH-$YEAR"
		CMD_DATE=" --expiredate $YEAR-$MONTH-$DAY"
		MOD=1
	elif [ "$DATE" == "n" ] || [ "$DATE" == "" ]; then
		DATE=""
		CMD_DATE=""
	else
		echo "Invalid option"
		return 1
	fi

	return 0
}

echo -e "\n===== Add user =====\n"

MOD=0

set_user
while [ $? != 0 ]; do
	set_user
done

set_home
while [ $? != 0 ]; do
	choose_home
done

set_shell
while [ $? != 0 ]; do
	set_shell
done

set_expire_date
while [ $? != 0 ]; do
	set_expire_date
done

#extra
echo "Extra options:"
read EXTRA

CMD="adduser$CMD_HOME_DIR$CMD_SHELL$EXTRA $CMD_USER_NAME"
CMD_MOD="usermod$CMD_DATE $CMD_USER_NAME"

echo -e "\nUser will be created with the following parameters:\n"
echo "====================================="
echo "username: $CMD_USER_NAME"
echo "Home directory: $HOME_DIR"
echo "Default login shell: $DEF_SHELL"
echo "Expire date: $DATE"
echo "Extra options: $EXTRA"
echo "====================================="

echo -e "\nCommand:\n$CMD"
echo -e "\nCreate user? [y/N]"

read DO_CREATE
if [ "$DO_CREATE" == y ]; then
	$CMD

	if [ $MOD == 1 ]; then
		$CMD_MOD
	fi

	echo "User '$CMD_USER_NAME' created!!"
	echo "You can remove this user with the command 'userdel $CMD_USER_NAME -r'"
fi

exit 0

