from app.functions.packer import pack, unpack
from app.signer import UrlSigner
import pika


def url_sign_callback(ch, method, props, body, signer: UrlSigner):
    body: dict = unpack(body)
    response = {"state": "INVALID", "error": "UNKNOWN"}
    complete = False

    # Check if reply_to is filled, if not we'll ignore message
    if not props.reply_to:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    while not complete:
        if "location" not in body:
            response["error"] = "MISSING-FIELD"
            complete = True
            continue
        else:
            match body["location"].get("region", None):
                case "FRA1":
                    path = body["location"].get("file_path", None)
                    if path:
                        file_split = path.split("/")
                        if file_split[0] == "vleedn":
                            url = signer.create_signed_link(path.replace("vleedn/", ""), "vleedn")
                            response = {
                                "state": "VALID",
                                "url": url
                            }
                            complete = True
                    else:
                        response["error"] = "MISSING-PATH"
                        complete = True
                        continue
                case _:
                    response["error"] = "MISSING-LOCATION"
                    complete = True
                    continue

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=pack(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
