extern crate google_sheets4 as sheets4;
use sheets4::api::ValueRange;
use sheets4::{Result, Error};
use std::default::Default;
use sheets4::{Sheets, oauth2, hyper, hyper_rustls, chrono, FieldMask};


#[tokio::main]
async fn main() {
    
    let sheet_id = "14s1FeqI--U8w0fdcCfeKOqSgwf59ZYwBaJUilSLSnSI";

    let secret= oauth2::read_service_account_key("C:\\Users\\bookw\\Downloads\\liquid-receiver.json").await.expect("key not found");
    let client = hyper::Client::builder().build(hyper_rustls::HttpsConnectorBuilder::new().with_native_roots().https_or_http().enable_http1().enable_http2().build());
    let auth = oauth2::ServiceAccountAuthenticator::with_client(secret, client.clone()).build().await.expect("auth failed");
    let hub = Sheets::new(client.clone(), auth);
    let result = hub.spreadsheets().values_get(sheet_id, "A1:A5").doit().await;
    
    match result {
        Err(e) => match e {
            // The Error enum provides details about what exactly happened.
            // You can also just use its `Debug`, `Display` or `Error` traits
            Error::HttpError(_)
            |Error::Io(_)
            |Error::MissingAPIKey
            |Error::MissingToken(_)
            |Error::Cancelled
            |Error::UploadSizeLimitExceeded(_, _)
            |Error::Failure(_)
            |Error::BadRequest(_)
            |Error::FieldClash(_)
            |Error::JsonDecodeError(_, _) => println!("{}", e),
        },
        Ok(res) => println!("Success: {:?}", res),
    }
}