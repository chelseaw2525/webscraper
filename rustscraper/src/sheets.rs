extern crate google_sheets4 as sheets4;
use yup_oauth2;
use sheets4::api::ValueRange;
use std::default::Default;
use sheets4::{Sheets, hyper, Error};
//use sheets4::{Result, hyper_rustls, chrono, FieldMask};

#[tokio::main]
async fn main() {

    let secret = yup_oauth2::read_application_secret("C:\\Users\\bookw\\Downloads\\liquid-receiver.json").await.expect("unreadable");
    let auth = yup_oauth2::InstalledFlowAuthenticator::builder(
        secret,
        yup_oauth2::InstalledFlowReturnMethod::HTTPRedirect,
    )
    .persist_tokens_to_disk("tokencache.json")
    .build()
    .await
    .unwrap();

    let hub = Sheets::new(hyper::Client::new(), auth,);

    let req = ValueRange::default();
    
    // You can configure optional parameters by calling the respective setters at will, and
    // execute the final call using `doit()`.
    // Values shown here are possibly random and not representative !
    let result = hub.spreadsheets().values_append(req, "1TdjbZZjEVkCuqMCOCz0cEVC-lUTi9RNBx_YZOoN2N2U", "Sheet1!A:A")
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