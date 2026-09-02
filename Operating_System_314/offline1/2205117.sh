#!/usr/bin/bash
alias bvcs='/home/rafin/Documents/os/2205117.sh '

usage(){
	echo "Command 			Description"
	echo "---------------------------------------------------------------------"
	echo "init 			Initialize a new BVCS repository"
	echo "add<file> 		Stage one or more files for the next commit"
	echo "status 			Show staged,modified and untracked files"
	echo "commit -m <msg> 		Save a snapshot of all staged files"
	echo "log 			Display the full commit history"
	echo "diff [file] 		Compare working copy to the latest commit"
	echo "restore <file>		Restore a file from the lates commit"
}
check_repo(){
	if [ ! -d ".bvcs" ]
	then
		echo "Error: Not a BVCS repository. Run 'init' first"
		exit 1
	fi
}



init_repo(){
	if [[ -d ".bvcs" ]]
	then
		echo "Error: BVCS repository already exists"
		exit 1
	else
		mkdir -p .bvcs/objects 
		touch .bvcs/staging .bvcs/log .bvcs/HEAD
		echo "Initalized empty BVCS repository"
	fi
}

add_file(){
	if [[ "$#" -eq 0 ]]
	then
		echo "Error: No files specified"
		exit 1
	fi
	for file in "$@"
	do
		if [[ ! -f "$file" ]]
		then
			echo "Error: '$file' not found"
			continue
		fi

		if grep -qxF "$file" .bvcs/staging 
		then
			echo "Already staged: $file"
		continue
		fi

		echo "$file" >> .bvcs/staging
		echo "Staged: $file"

	done
}



show_status(){
	declare -A file_status
	declare -A head_files

	if [[ -f ".bvcs/staging" && -s ".bvcs/staging" ]]
	then
		while IFS= read -r file
		do
			if [[ ! -z "$file" ]]
			then
				file_status["$file"]="staged"
			fi
		done < .bvcs/staging

	fi

	local head_commits=""
	if [[ -f ".bvcs/HEAD" && -s ".bvcs/HEAD" ]]
	then

		head_commits=$(cat .bvcs/HEAD)
	fi

	if [[ -n "$head_commits" ]]
	then
		local snapshot_dir=".bvcs/objects/$head_commits/files"

		if [[ -d "$snapshot_dir" ]]
		then

			while IFS= read -r snap_file
			do
			if [[ -n "$snap_file" ]]
			then

				local relative_path="${snap_file#$snapshot_dir/}"
				head_files["$relative_path"]=1

				if [[ "${file_status["$relative_path"]}" != "staged" ]]
				then
					if [[ -f "$relative_path" ]]
					then

						if ! cmp -s "$relative_path"  "$snap_file"
						then

							file_status["$relative_path"]="modified"
						fi
					else
						file_status["$relative_path"]="modified"

					fi

				fi

			fi
			done < <(find "$snapshot_dir" -type f | sort)

		fi



	fi

	while IFS= read -r working_file
	do

		if [[ -n "$working_file" ]]
		then


			local relative_path="${working_file#./}"

			if [[ -z "${file_status["$relative_path"]}" && -z "${head_files["$relative_path"]}" ]]
			then

				file_status["$relative_path"]="untracked"

			fi


		fi



	done < <(find . -type f -not -path './.bvcs*' 2>/dev/null)



	local staged=()
	local modified=()
	local untracked=()

	local sorted_files

	sorted_files=$(echo "${!file_status[@]}" | tr ' ' '\n' | sort)

	for file in $sorted_files
	do

		[[ -z "$file" ]] && continue
		case "${file_status["$file"]}" in
			staged)
				staged+=("$file");;
			modified)
				modified+=("$file");;

			untracked)
				untracked+=("$file");;
		esac

	done

	local output=false
	if [[ ${#staged[@]} -gt 0 ]] 
	then

		echo "Staged for commit:"
		for file in "${staged[@]}"
		do
			echo "$file"

		done
		output=true

	fi

	if [[ ${#modified[@]} -gt 0 ]]
	then
                [[ "$output" == true ]] && echo ""
                	echo "Modified (not staged):"
                for file in "${modified[@]}"
		do

		         echo "$file"
                done
                output=true
        fi
	if [[ ${#untracked[@]} -gt 0 ]]
	then
                [[ "$output" == true ]] && echo ""
                echo "Untracked files:"

	        for file in "${untracked[@]}"
	        do
                        echo "$file"
                done
                output=true
        fi


        if [[ "$output" == false ]]
	then
                echo "Nothing to commit, working tree clean"
        fi
}


do_commit(){
	local message=""

	while [[ $# -gt 0 ]]
	do

		case "$1" in
           		 -m)
               			 shift
               			 [[ -z "$1" ]] && {
                   		 echo 'Error: Commit message required. Use -m "message".'
                   		 exit 1
               			 }
               			 message="$1"
               			 ;;
           		 *)
               			 echo 'Error: Commit message required. Use -m "message".'
               			 exit 1
               			 ;;
       		 esac
       		 shift
	done

	if [[ -z "$message" ]]
	then
        	echo 'Error: Commit message required. Use -m "message".'
       		 exit 1
   	 fi

	if [[ ! -s .bvcs/staging ]]
	then
        	echo "Error: Nothing to commit."
        	exit 1
   	 fi

	if [[ -s .bvcs/HEAD ]]
	then
   		last=$(cat .bvcs/HEAD)
    		id=$(printf "%04d" $((10#$last + 1)))
	else
    		id="0001"
	fi

	snapshot=".bvcs/objects/$id/files"
	mkdir -p "$snapshot"
	if [[ -n "$last" ]]
	then
    		cp -a ".bvcs/objects/$last/files/." "$snapshot/"
	fi

	count=0

	while IFS= read -r file
	do
    		[[ -z "$file" ]] && continue

    		mkdir -p "$snapshot/$(dirname "$file")"
    		cp "$file" "$snapshot/$file"

    		((count++))
	done < .bvcs/staging

	echo "$message" > ".bvcs/objects/$id/message"

	date '+%Y-%m-%d %H:%M:%S' > ".bvcs/objects/$id/timestamp"

	timestamp=$(cat ".bvcs/objects/$id/timestamp")

	echo "$id|$timestamp|$message" >> .bvcs/log

	echo "$id" > .bvcs/HEAD

	> .bvcs/staging

	echo "[$id] $message"
	echo "$count file(s) committed"

}


show_log() {

   	 if [[ ! -s .bvcs/log ]]
	then
        	echo "No commits yet."
        return
    	fi

    	tac .bvcs/log | while IFS='|' read -r id timestamp message
    	do
        	echo "commit $id"
        	echo "Date: $timestamp"
        	echo "Message: $message"
        	echo
    	done
}


show_diff(){


	if [[ ! -s .bvcs/HEAD ]]
	then

		echo "Error: No commits yet."
		return 1
	fi

	head=$(cat .bvcs/HEAD)
	snapshot=".bvcs/objects/$head/files"

	file="$1"

	if [[ -n "$file" ]] 
	then

		if [[ ! -f "$snapshot/$file" ]] 
		then

			echo "Error: '$file' is not tracked"
			return 1

		fi

		if diff -q "$snapshot/$file" "$file" > /dev/null
		then
			echo "$file: no changes."
		else
			diff -u \
			--label "$snapshot/$file" \
			--label "$file" \
			"$snapshot/$file" "$file"
		fi

	else


		while IFS= read -r tracked
		do
			relative="${tracked#$snapshot/}"
			if diff -q "$tracked" "$relative" >/dev/null
			then

				echo "$relative:no changes."
			else
				diff -u \
					--label "$tracked"
					--label "$relative"
					"$tracked" "$relative"
			fi

		done < <(find "$snapshot" -type f | sort)

	fi

}


try_restore(){


	if [[ -z "$1" ]]
        then
                echo "Error: No file specified."
                return 1

        fi

	if [[ ! -s ".bvcs/HEAD" ]]
	then

		echo "Error: no commits yet."
		return 1

	fi

	head=$(cat .bvcs/HEAD)
	filename="$1"
	snapshot=".bvcs/objects/$head/files/$filename"



	if [[ ! -f "$snapshot" ]]
	then
		echo "Error: '$filename' not found in commit $head"
		return 1
	fi
	read -p "Restore '$filename' from commit $head? [Y/N]: " abc


	if [[ "$abc" == "y" || "$abc" == "Y" ]]
	then

		mkdir -p "$(dirname "$filename")"
		cp "$snapshot" "$filename"
		echo "Restored: $filename"
	else
		echo "Aborted."
	fi



}



case "$1" in
	init)
		init_repo;;
	check)
		check_repo;;
	add)
		check_repo
		add_file "${@:2}";;
	status)
		check_repo
		show_status;;
	commit)
		check_repo
		shift
		do_commit "$@";;
	log)
		check_repo
		show_log;;
	diff)
		check_repo
		shift
		show_diff "$@";;
	help)
		usage
		;;
	restore)
		check_repo
		try_restore "$2";;
	*)
		echo "Error: Unknown subcommand '$1'"
		exit 1

esac
