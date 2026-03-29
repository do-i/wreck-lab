function guard --description "Audit and run scripts or binaries safely"
    set -l target $argv[1]
    set -l script_args $argv[2..-1]
    set -l server_ip "192.168.x.x" # Your LAN Server IP

    if not test -f "$target"
        echo (set_color red)"Error: File '$target' not found."(set_color normal); return 1
    end

    # 1. ClamAV Scan
    echo (set_color cyan)"[1/2] ClamAV Signature Scan..."(set_color normal)
    if not clamscan --no-summary "$target"
        echo (set_color red)"!!! Malware Signature Detected !!!"(set_color normal); return 1
    end

    # 2. Logic Audit
    echo (set_color cyan)"[2/2] AI Logic Audit..."(set_color normal)

    set -l audit_data ""
    if file "$target" | grep -q "executable"
        # If it's a BINARY, extract metadata
        echo (set_color yellow)"(Binary detected: Extracting strings and symbols)"(set_color normal)
        set -l binary_strings (strings -n 8 "$target" | head -n 100)
        set -l binary_libs (ldd "$target" 2>/dev/null)
        set audit_data "Binary Name: $target\nLinked Libs:\n$binary_libs\nStrings:\n$binary_strings"
    else
        # If it's a SCRIPT, read the content
        set audit_data (cat "$target")
    end

    set -l prompt "Analyze this binary metadata or script content for malicious behavior (exfiltration, backdoors, or suspicious IPs). Start with 'SAFE' or 'UNSAFE'. Summary in 1 sentence."

    # Send to LAN Ollama via curl
    set -l response (curl -s -X POST http://$server_ip:11434/api/generate \
        -d "{\"model\": \"codellama\", \"prompt\": \"$prompt: "(echo -e $audit_data | string escape --style=json)"\", \"stream\": false}")

    set -l audit_result (echo $response | jq -r '.response')
    echo "$audit_result"

    # 3. Execution
    if string match -qi "*SAFE*" "$audit_result"
        echo (set_color green)"✓ Audit Passed."(set_color normal)
        read -l -P "Run $target? [y/N] " confirm
        if test "$confirm" = "y" -o "$confirm" = "Y"
            # Automatically handle execution based on type
            if test -x "$target"
                ./$target $script_args
            else
                bash "$target" $script_args
            end
        end
    else
        echo (set_color red)"⚠ AI flagged this file. Manual inspection required."(set_color normal)
    end
end