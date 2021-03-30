# coding: utf-8

# flake8: noqa

"""
    Klippa Custom OCR API

    # Introduction The Klippa Custom OCR Webservice API is a REST webservice for custom OCR implementations by Klippa.  The service replies are JSON only.  The service base URL is https://custom-ocr.klippa.com/api/v1. The service base URL for the test environment is https://test.custom-ocr.klippa.com/api/v1, we test experimental templates and features there. It also hosts the demo interface.  # Authentication ## APIKeyHeader The API requires the following header to be set:  Header | Description | --- |--- |   X-Auth-Key  |  The auth key provided by Klippa. |  The Key is provided per customer by Klippa.  ## APIKeyQueryParam The key can also be provided in the request query as ```?X-Auth-Key=key```  ## APIPublicKeyHeader The Public API requires the following header to be set:  Header | Description | --- |--- |   X-Auth-Public-Key  |  The public auth key provided by Klippa. |  ## APIPublicKeyQueryParam The key can also be provided in the request query as ```?X-Auth-Public-Key=public-key```   # Calling the API from public applications If you want to call the API from a public application, like a mobile app, you should **NOT** embed your API key in the app, this key could be extracted and abused.  The way to do this is using our API to [generate a public key](#operation/createPublicKey) from your backend, and send that public key to your application. That way only users that are authenticated are allowed to call the API. That way you can also better monitor which users are using the API and prevent abuse. You can also configure the public key to be valid for a certain time and give a maximum amount of scans.  The public key API is not available for every API key, we have to enable this for you.  We also have a [complete scanner SDK for Android and iOS](https://www.klippa.com/en/ocr/ocr-sdk/) available that has this API integrated.  The Public API requires the following header to be set:  Header | Description | --- |--- |   X-Auth-Public-Key  |  The public auth key provided by Klippa. |  The key can also be provided in the request query as ```?X-Auth-Public-Key=public-key```   # API Client libraries  Language | Client | --- |--- |   Go  |   [go.tar.gz](/docs/static/clients/go.tar.gz) |   Java  |   [java.tar.gz](/docs/static/clients/java.tar.gz) |   PHP  |   [php.tar.gz](/docs/static/clients/php.tar.gz) |   Python  |   [python.tar.gz](/docs/static/clients/python.tar.gz) |   Typescript (Axios)  |   [typescript.tar.gz](/docs/static/clients/typescript.tar.gz) |   Swift 4  |   [swift4.tar.gz](/docs/static/clients/swift4.tar.gz) |   Swift 5  |   [swift5.tar.gz](/docs/static/clients/swift5.tar.gz) |   # Error codes ## Authentication errors  Code | Name | --- |--- |   100001  |   ErrorCodeAuthMissingKey |   100002  |   ErrorCodeAuthInvalidKey |   100003  |   ErrorCodeAuthError |   100004  |   ErrorCodeAuthNoCreditsLeft |   100005  |   ErrorCodeAuthInvalidPublicKey |   100006  |   ErrorCodeAuthPublicKeyNoScansLeft |   100007  |   ErrorCodeAuthPublicKeyExpired |   ## PDF Parser errors  Code | Name | --- |--- |   200001  |   ErrorCodePDFParserDocumentError |   200002  |   Obsolete |   200003  |   Obsolete |   200004  |   ErrorCodePDFParserNoAccessToTemplate |   200005  |   ErrorCodePDFParserConvertError |   200006  |   ErrorCodePDFParserParseError |   ## Document Parser errors  Code | Name | --- |--- |   300001  |   ErrorCodeDocumentParserDocumentError |   300002  |   Obsolete |   300003  |   Obsolete |   300004  |   ErrorCodeDocumentParserNoAccessToTemplate |   300005  |   ErrorCodeDocumentParserConvertError |   300006  |   ErrorCodeDocumentParserParseError |   300007  |   ErrorCodeDocumentParserTooBigFileError |   ## Public Key errors  Code | Name | --- |--- |   400001  |   ErrorCodePublicKeyNotAllowed |   400002  |   ErrorCodePublicKeyCreationFailed |   400003  |   ErrorCodePublicKeyInvalidScanLimit |   400004  |   ErrorCodePublicKeyInvalidValidTime |   400005  |   ErrorCodePublicKeyLoadError |   400006  |   ErrorCodePublicKeyNotFoundError |  # Userdata  The user_data field allows for sending additional data into the parser and can be used to enable extra features, improve the recognition of certain fields and improve the processing speed. The user_data must be given as a JSON-encoded string. All fields are optional, a document may be submitted without this field.  The following fields are accepted in the user_data object:  Key | Value type  | Description | --|--|--| `client`| `Relation` object | A relation object containing information about the client that submits the document. It should contain information either the merchant of the customer of the invoice. This is indicated by the `transaction_type` key. If the `transaction_type` is set to `purchase`, the client is considered to be the customer. If the `transaction_type` is set to `sale`, the client is considered to be the merchant. `transaction_type`  | string  | The transaction type of the document for the client. If the invoices contains a sale that the client made, this field can be set to `sale`. If the invoice contains a purchase that the client made, this field can be set to `purchase`.| `relations`  | array of `Relation` objects  | An optional list of relations which have previously been used by the client. The list does not have to be complete, the OCR may suggest merchants and customers which are not in this list. | `transactions`  | array of `Transaction` objects  | An optional list of open transactions for the client. We use this list to validate and improve our OCR detections. | `purchase_orders`  | array of `PurchaseOrder` objects  | An optional list of purchase orders. It's identifier will be present in the output if the purchase order was found on the document | `locale`| `Locale` object | If the language or originating country of the document is known, these values may be set.   ## Relation object  The relation object may contain the following fields. All fields are optional and may be omitted if a field is not available. This user data can also be managed by [User Data Sets](#tag/UserDataSets) when allowed for your key.  Key | Value type  | Description | --|--|--| id|string|The ID of the relation in your own system, we will return this id in the `merchant_id` field if there is a match. In the User Data Set this is the ExternalID. name|string|The company name of the client street_name|string|The street name of the client address street_number|string|The street number of the client address zipcode|string|The zipcode of the client address city|string|The city of the client address country|string|The country of the client address. It must be provided as a 2-letter country code as specified by ISO 3166-1. For example `FR` for France and `NL` for The Netherlands vat_number|string|The vat number, formatted according to the EU VAT directive. It must start with the country code prefix, such as `FR` or `NL` coc_number|string|A chamber of commerce number. E.g. the Dutch KVK number, or the French SIRET/SIREN number phone|string|The phone number of the client. International calling codes, such as `+33` may be provided but are not required website|string|The full URL to the website email|string|The email address bank_account_number|string|The IBAN number   ## Transaction object  The transaction object may contain the following fields. All fields are optional and may be omitted if a field is not available. This user data can also be managed by [User Data Sets](#tag/UserDataSets) when allowed for your key.  Key | Value type  | Description | --|--|--| identifier|string|The identifier of the transaction as given by the bank date|string|The date of the transaction, in the format 2019-06-24 11:16:33 currency|string|The currency of the transaction, eg. EUR amount|float|The amount of the transaction, eg 23.56 description|string|The description of the transaction as given by the bank iban|string|The IBAN number that made the transaction name|string|The name of the bank account  ## PurchaseOrder object  The PurchaseOrder object may contain the following fields. The `date` and `amount` fields are optional. If given, the purchase order will only be searched for on the document if those fields match the document date and document total amount, respectively.  Key | Value type  | Description | --|--|--| identifier|string|The identifier of the purchase order purchase_order_number|string|The purchase order number which should be searched for on the document, e.g 'PO-12345' date|string|The expected document date, in the format 2019-06-24 11:16:33 amount|float|The expected total amount on the document, eg 23.56   ## Locale object In case the language and/or originating country of the document are known, these may be set in the locale object. The locale object may contain the following fields. Both fields are optional.  Key | Value type  | Description | --|--|--| language|string|A 2-letter language code according to ISO 3166-1. country|string|A 2-letter country code according to ISO 639.  ## Keyword and lineitem matching Keyword rules can be use to find strings in the text of the document using either a list of keywords or a regex.  Multiple rules may be given, each rule will provide a separate object in the output. All keywords and regexes are treated case-insensitive.  For example, by passing the following `keywords_rules` object, the regex will match all \"new product\" strings which are followed by a number. The matches are provided in the output in an object with \"id\" set to \"products\". The \"coupon\" rule can be used to count the number of occurrences of a list of words:  ``` { \"keyword_rules\": [ { \"id\": \"products\", \"regex\": \"(new product [0-9]+)\" }, { \"id\": \"coupon\", \"keywords\": [ \"coupon\" ] } ] } ```  If for example the keywords of \"products\" are matched 3 times in the text of the document, and the keywords of \"coupons\" 2 times, the output will be: ``` { \"matched_keywords\": [ { \"id\": \"products\", \"count\": 3 \"matches\": [\"new product 6\", \"new product 1\", \"new product 14\"] }, { \"id\": \"coupons\", \"count\": 2 \"matches\": [\"COUPON\", \"coupon\"] } ] } ```  ### Lineitem matching Similar to keyword rules, lineitems rules can be used to list products which contain a certain keyword. ``` { \"lineitem_rules\": [ { \"id\": \"fruit\", \"regex\": \"apple|banana\" }, { \"id\": \"vegetables\", \"keywords\": [ \"carrots\", \"broccoli\" ] } ] } ``` For example, if some of the lineitems on the document contain a word that is in the \"vegetables\" keyword list, they are of the present in the output under the \"vegetables\" key: ``` { \"matched_lineitems\": [ { \"id\": \"vegetables\", \"lineitems\": [ { \"title\": \"1kg carrots\", \"amount\": 164, \"amount_each\": 82, \"quantity\": 2 }, { \"title\": \"Set of 2 broccoli\", \"amount\": 164, \"amount_each\": 592, \"quantity\": 4 } ] } ] } ```  ## Userdata Example ``` { \"client\": { \"name\": \"\", \"street_name\": \"\", \"street_number\": \"\", \"zipcode\": \"\", \"city\": \"\", \"country\": \"\", \"vat_number\": \"\", \"coc_number\": \"\", \"phone\": \"\", \"website\": \"\", \"email\": \"\", \"bank_account_number\": \"\" }, \"transaction_type\": \"\", \"relations\": [ { \"name\": \"\", \"street_name\": \"\", \"street_number\": \"\", \"zipcode\": \"\", \"city\": \"\", \"country\": \"\", \"vat_number\": \"\", \"coc_number\": \"\", \"phone\": \"\", \"website\": \"\", \"email\": \"\", \"bank_account_number\": \"\" }, { \"name\": \"\", \"street_name\": \"\", \"street_number\": \"\", \"zipcode\": \"\", \"city\": \"\", \"country\": \"\", \"vat_number\": \"\", \"coc_number\": \"\", \"phone\": \"\", \"website\": \"\", \"email\": \"\", \"bank_account_number\": \"\" } ], \"locale\": { \"language\": \"\", \"country\": \"\" } } ```  # noqa: E501

    The version of the OpenAPI document: v0-15-73 - 4af1fa1031af2e5c7f586e672cffa86481c87b0c
    Contact: jeroen@klippa.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

__version__ = "1.0.0"

# import apis into sdk package
from klippa_ocr_api.api.information_api import InformationApi
from klippa_ocr_api.api.parsing_api import ParsingApi
from klippa_ocr_api.api.public_key_api import PublicKeyApi
from klippa_ocr_api.api.sub_key_api import SubKeyApi
from klippa_ocr_api.api.user_data_sets_api import UserDataSetsApi

# import ApiClient
from klippa_ocr_api.api_client import ApiClient
from klippa_ocr_api.configuration import Configuration
from klippa_ocr_api.exceptions import OpenApiException
from klippa_ocr_api.exceptions import ApiTypeError
from klippa_ocr_api.exceptions import ApiValueError
from klippa_ocr_api.exceptions import ApiKeyError
from klippa_ocr_api.exceptions import ApiException
# import models into sdk package
from klippa_ocr_api.models.api_index import APIIndex
from klippa_ocr_api.models.api_index_body import APIIndexBody
from klippa_ocr_api.models.barcode import Barcode
from klippa_ocr_api.models.bulk_user_data_set_record_action_form import BulkUserDataSetRecordActionForm
from klippa_ocr_api.models.bulk_user_data_set_record_body import BulkUserDataSetRecordBody
from klippa_ocr_api.models.bulk_user_data_set_record_form import BulkUserDataSetRecordForm
from klippa_ocr_api.models.bulk_user_data_set_record_result import BulkUserDataSetRecordResult
from klippa_ocr_api.models.create_public_key import CreatePublicKey
from klippa_ocr_api.models.create_public_key_body import CreatePublicKeyBody
from klippa_ocr_api.models.create_public_key_form import CreatePublicKeyForm
from klippa_ocr_api.models.create_sub_key_body import CreateSubKeyBody
from klippa_ocr_api.models.create_user_data_set_form import CreateUserDataSetForm
from klippa_ocr_api.models.create_user_data_set_record_form import CreateUserDataSetRecordForm
from klippa_ocr_api.models.create_user_data_set_record_response_body import CreateUserDataSetRecordResponseBody
from klippa_ocr_api.models.create_user_data_set_response_body import CreateUserDataSetResponseBody
from klippa_ocr_api.models.delete_sub_key_body import DeleteSubKeyBody
from klippa_ocr_api.models.delete_user_data_set_body import DeleteUserDataSetBody
from klippa_ocr_api.models.delete_user_data_set_record_body import DeleteUserDataSetRecordBody
from klippa_ocr_api.models.deleted_object_data import DeletedObjectData
from klippa_ocr_api.models.error import Error
from klippa_ocr_api.models.european_passport import EuropeanPassport
from klippa_ocr_api.models.european_passport_body import EuropeanPassportBody
from klippa_ocr_api.models.full_identity_document import FullIdentityDocument
from klippa_ocr_api.models.get_credits import GetCredits
from klippa_ocr_api.models.get_credits_body import GetCreditsBody
from klippa_ocr_api.models.get_field import GetField
from klippa_ocr_api.models.get_field_subtype import GetFieldSubtype
from klippa_ocr_api.models.get_fields import GetFields
from klippa_ocr_api.models.get_fields_body import GetFieldsBody
from klippa_ocr_api.models.get_public_key_info import GetPublicKeyInfo
from klippa_ocr_api.models.get_public_key_info_body import GetPublicKeyInfoBody
from klippa_ocr_api.models.get_statistics_body import GetStatisticsBody
from klippa_ocr_api.models.get_sub_key_body import GetSubKeyBody
from klippa_ocr_api.models.get_templates import GetTemplates
from klippa_ocr_api.models.get_templates_body import GetTemplatesBody
from klippa_ocr_api.models.get_user_data_set_body import GetUserDataSetBody
from klippa_ocr_api.models.get_user_data_set_record_body import GetUserDataSetRecordBody
from klippa_ocr_api.models.get_user_data_set_records import GetUserDataSetRecords
from klippa_ocr_api.models.get_user_data_set_records_body import GetUserDataSetRecordsBody
from klippa_ocr_api.models.get_user_data_sets import GetUserDataSets
from klippa_ocr_api.models.get_user_data_sets_body import GetUserDataSetsBody
from klippa_ocr_api.models.identity_document import IdentityDocument
from klippa_ocr_api.models.identity_document_body import IdentityDocumentBody
from klippa_ocr_api.models.identity_document_image import IdentityDocumentImage
from klippa_ocr_api.models.identity_document_image_and_value import IdentityDocumentImageAndValue
from klippa_ocr_api.models.identity_document_string_value import IdentityDocumentStringValue
from klippa_ocr_api.models.key import Key
from klippa_ocr_api.models.matched_keyword import MatchedKeyword
from klippa_ocr_api.models.matched_line_items_receipt import MatchedLineItemsReceipt
from klippa_ocr_api.models.public_key_statistics_body import PublicKeyStatisticsBody
from klippa_ocr_api.models.receipt import Receipt
from klippa_ocr_api.models.receipt_body import ReceiptBody
from klippa_ocr_api.models.receipt_line_item import ReceiptLineItem
from klippa_ocr_api.models.receipt_line_item_item import ReceiptLineItemItem
from klippa_ocr_api.models.receipt_vat import ReceiptVAT
from klippa_ocr_api.models.resp_template import RespTemplate
from klippa_ocr_api.models.stat_row import StatRow
from klippa_ocr_api.models.sub_key_form import SubKeyForm
from klippa_ocr_api.models.sub_key_list_body import SubKeyListBody
from klippa_ocr_api.models.sub_key_statistics_body import SubKeyStatisticsBody
from klippa_ocr_api.models.sub_keys import SubKeys
from klippa_ocr_api.models.template import Template
from klippa_ocr_api.models.text_upload_form import TextUploadForm
from klippa_ocr_api.models.update_sub_key_body import UpdateSubKeyBody
from klippa_ocr_api.models.update_user_data_set_body import UpdateUserDataSetBody
from klippa_ocr_api.models.update_user_data_set_form import UpdateUserDataSetForm
from klippa_ocr_api.models.update_user_data_set_record_body import UpdateUserDataSetRecordBody
from klippa_ocr_api.models.update_user_data_set_record_form import UpdateUserDataSetRecordForm
from klippa_ocr_api.models.user_data_set import UserDataSet
from klippa_ocr_api.models.user_data_set_record import UserDataSetRecord
from klippa_ocr_api.models.user_data_set_record_value_form import UserDataSetRecordValueForm
from klippa_ocr_api.models.validation_error import ValidationError

