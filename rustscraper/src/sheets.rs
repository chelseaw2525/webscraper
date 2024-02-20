extern crate google_sheets4 as sheets4;
use sheets4::api::ValueRange;
use sheets4::{Result, Error};
use std::default::Default;
use sheets4::{Sheets, oauth2, hyper, hyper_rustls, chrono, FieldMask};
use sheets4::oauth2::authenticator::Authenticator;
use config::Config;


#[tokio::main]
async fn main() {
    let secret= oauth2::parse_service_account_key("C:\\Users\\bookw\\Downloads\\client-secret.json").unwrap();
    let auth = oauth2::InstalledFlowAuthenticator::builder(
        secret,
        oauth2::InstalledFlowReturnMethod::HTTPRedirect,
    ).build().await.unwrap();
    let mut hub = Sheets::new(hyper::Client::builder().build(hyper_rustls::HttpsConnectorBuilder::new().with_native_roots().https_or_http().enable_http1().build()), auth);
    let mut req = ValueRange::default();
    let result = hub.spreadsheets().values_append(req, "spreadsheetId", "range")
             .value_input_option("amet.")
             .response_value_render_option("duo")
             .response_date_time_render_option("ipsum")
             .insert_data_option("gubergren")
             .include_values_in_response(true)
             .doit().await;
    
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