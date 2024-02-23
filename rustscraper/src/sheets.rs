extern crate google_sheets4 as sheets4;
use config::Value;
use sheets4::api::ValueRange;
use sheets4::Error;
use sheets4::{Sheets, oauth2, hyper, hyper_rustls};
use std::time::*;

#[tokio::main]
async fn main() {
    let now = Instant::now();
    let sheet_id = "14s1FeqI--U8w0fdcCfeKOqSgwf59ZYwBaJUilSLSnSI";

    let secret= oauth2::read_service_account_key("C:\\Users\\bookw\\Downloads\\liquid-receiver.json").await.expect("key not found");
    let client = hyper::Client::builder().build(hyper_rustls::HttpsConnectorBuilder::new().with_native_roots().https_or_http().enable_http1().enable_http2().build());
    let auth = oauth2::ServiceAccountAuthenticator::with_client(secret, client.clone()).build().await.expect("auth failed");
    let hub = Sheets::new(client.clone(), auth);
    let result = hub.spreadsheets().values_get(sheet_id, "A1:A6").doit().await;
    
    match result {
        Err(e) => println!("{}", e),
        Ok((_, data)) => println!("results: {:?}", data.values.unwrap()),
    }

    let elapsed_time = now.elapsed();
    println!("Time @ {} microsec.", elapsed_time.as_micros());
    
    let mut req = ValueRange{major_dimension: Some("ROWS".to_owned()), values: Some(vec![vec![Into::into("ferris"), Into::into("corro")]]), range: Some(String::from("A1:A6"))};    
    let result = hub.spreadsheets().values_append( req, sheet_id, "A1:A6").value_input_option("USER_ENTERED").doit().await;
}
