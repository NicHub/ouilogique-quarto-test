#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

###
#
# This script starts a Quarto preview server.
#
# - it finds an available host_port (starting from 4444 by default),
# - detects the IPv4 address of the default network interface,
# - prints the preview URL and its QR code,
# - then launches `quarto preview`.
#
# Works on macOS only.
#
# Usage:
#     bash _serve.sh
#     bash _serve.sh [start_port] [port_count]
#
##

###
# Scratchpad:
#
# quarto preview --host_port 4444
# rm -rf _site && quarto preview --host_port 4444
# quarto render index.qmd
##

# Find the first free TCP host_port from a starting host_port,
# within a bounded range.
get_first_free_tcp_port() {
    local start_port="${1:-4444}"
    local port_count="${2:-10}"
    local host_port

    for ((host_port = start_port; host_port < start_port + port_count; host_port++)); do
        if ! lsof -nP -iTCP:"${host_port}" -sTCP:LISTEN >/dev/null 2>&1; then
            echo "${host_port}"
            return 0
        fi
    done

    echo "Error: no free host_port found between ${start_port} and" \
        "$((start_port + port_count - 1))." >&2
    exit 1
}

get_ip_of_default_interface() {
    local default_iface
    local ip_addr

    default_iface="$(
        route -n get default 2>/dev/null | awk '/interface: / {print $2; exit}'
    )"

    if [[ -z "${default_iface}" ]]; then
        echo "Error: unable to find the default network interface." >&2
        exit 1
    fi

    ip_addr="$(ipconfig getifaddr "${default_iface}" 2>/dev/null || true)"

    if [[ -z "${ip_addr}" ]]; then
        ip_addr="$(
            ifconfig "${default_iface}" 2>/dev/null |
                awk '/inet / && $2 != "127.0.0.1" {print $2; exit}'
        )"
    fi

    if [[ -z "${ip_addr}" ]]; then
        echo "Error: unable to get an IPv4 address for ${default_iface}." >&2
        exit 1
    fi

    echo "${ip_addr}"
}

show_preview_url_and_qr() {
    local host_ip="${1}"
    local host_port="${2}"
    local preview_url
    preview_url="http://${host_ip}:${host_port}/"

    echo "Preview URL: ${preview_url}"

    if command -v qrencode >/dev/null 2>&1; then
        qrencode -t ANSIUTF8 "${preview_url}"
        return 0
    fi

    echo "Error: qrencode is required to print the QR code." >&2
    echo "Install it with: brew install qrencode" >&2
    exit 1
}

run_quarto_preview() {
    local host_ip="${1}"
    local host_port="${2}"

    quarto preview \
        --host "${host_ip}" \
        --port "${host_port}"
}

main() {
    local start_port="${1:-4444}"
    local port_count="${2:-10}"
    local host_port
    local ip_of_default_interface

    host_port="$(get_first_free_tcp_port "${start_port}" "${port_count}")"
    ip_of_default_interface="$(get_ip_of_default_interface)"

    show_preview_url_and_qr "${ip_of_default_interface}" "${host_port}"
    run_quarto_preview "${ip_of_default_interface}" "${host_port}"
}

main "$@"
