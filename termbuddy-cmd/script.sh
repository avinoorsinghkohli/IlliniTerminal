split_iterm() {
    osascript <<EOF
tell application "iTerm2"
    if (count of windows) = 0 then
        create window with default profile
    end if
    tell current window
        tell current session
            set firstPane to split horizontally with default profile
            tell firstPane
                split vertically with default profile
            end tell
        end tell
    end tell
end tell
EOF
}

termbuddy_fn()  {
    if [ $# -eq 0 ]; then
        echo "Usage: stream_output <command>" >&2
        return 1
    fi

    local combined_file="$HOME/.combined_output.txt"

    # Execute the command and capture output
    set -o pipefail
    { "$@" 2>&1 | tee "${combined_file}"; } 3>&1
    local exit_status=$?
    set +o pipefail

    if [ $exit_status -ne 0 ]; then
        echo -e "\033[31m"
        echo "We noticed that you faced an error! here are some suggestions - " >&2
        echo -e "\033[0m"
        ENDPOINT="http://127.0.0.1:5001/generate?code_file=&error_file=$HOME/.combined_output.txt"

        # Make the GET request using curl
        response=$(curl -s -w "\n%{http_code}" $ENDPOINT)

        # Extract the response body and status code
        body=$(echo "$response" | sed -e '$d')
        status_code=$(echo "$response" | tail -n1)

        # Print the results
        # echo "Response body:"
        # echo -e "\033[33m"
        echo "=============================================================================================================="
        echo "$body" | glow - -w 100 
        echo "=============================================================================================================="

        # echo -e "\033[0m"
        # echo "Status code: $status_code"

        # Check if the request was successful
        if [ $status_code -eq 200 ]; then
            # echo "Request successful"
        else
            echo "Sorry we cannot fetch suggestions $status_code"
        fi
        return $exit_status
    fi
}

termbuddy_retry()  {
    
    ENDPOINT="http://127.0.0.1:5001/retry?code_file=&error_file=$HOME/.combined_output.txt"

    # Make the GET request using curl
    response=$(curl -s -w "\n%{http_code}" $ENDPOINT)

    # Extract the response body and status code
    body=$(echo "$response" | sed -e '$d')
    status_code=$(echo "$response" | tail -n1)

    # Print the results
    # echo "Response body:"
    # echo -e "\033[33m"
    echo "=============================================================================================================="
    echo "$body" | glow - -w 100 
    echo "=============================================================================================================="

    # echo -e "\033[0m"
    # echo "Status code: $status_code"

    # Check if the request was successful
    if [ $status_code -eq 200 ]; then
        # echo "Request successful"
    else
        echo "Sorry we cannot fetch suggestions $status_code"
    fi
    return $exit_status
    
}


alias termbuddy='termbuddy_fn' 
alias tb='termbuddy_fn' 
alias tb-retry='termbuddy_retry' 