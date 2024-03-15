extern crate google_sheets4 as sheets4;
use sheets4::api::ValueRange;
use sheets4::{Sheets, oauth2, hyper, hyper_rustls};
use std::time::*;
use std::error::Error;
use thirtyfour::*;
use futures::future::*;
use std::{thread, u16, time, error};

#[tokio::main]
async fn main() {
    let data = searcher().await.unwrap();
    sheets(data).await;
}

async fn sheets(values: Vec<String>) {
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
    
    let req = ValueRange{major_dimension: Some("ROWS".to_owned()), values: Some(vec![vec![Into::into("ferris"), Into::into("corro")]]), range: Some(String::from("A1:A6"))};    
    let _result = hub.spreadsheets().values_append( req, sheet_id, "A1:A6").value_input_option("USER_ENTERED").doit().await;
}

static TARGET: &str = "https://www.google.com/search?newwindow=1&sca_esv=94cc259175ff0bb8&q=best+restaurants+denver&tbm=nws&source=lnms&prmd=hminvsbtz&sa=X&ved=2ahUKEwjl9czZ0_WEAxVxhu4BHRvnCDYQ0pQJegQIExAB&biw=1920&bih=937";

async fn searcher()->  Result<Vec<String>, Box<dyn Error + Send + Sync>> {
    let mut list = Vec::new();
    let mut caps = DesiredCapabilities::firefox();
    caps.add_firefox_arg("--enable-automation")?;
    let driver = WebDriver::new("http://localhost:4444", caps).await?;

    driver.goto::<&str>(TARGET.as_ref()).await?;

    list = grab_page(driver.clone(), list).await.unwrap();

    next_page(driver.clone(), 2).await?;
    list = grab_page(driver.clone(), list).await.unwrap();

    next_page(driver.clone(), 3).await?;
    list = grab_page(driver.clone(), list).await.unwrap();

    println!("number {}, return vals: {:?}", list.len(), list);
    driver.quit().await?;

    Ok(list)
}

async fn grab_page(driver: WebDriver, list: Vec<String>)->  Result<Vec<String>, Box<dyn Error + Send + Sync>> {
    let mut list = list;
    let elem = driver.find_all(By::XPath("/html/body/div[5]/div/div[11]/div/div[2]/div[2]/div/div/div/div/div/div/div/a")).await?;
    let elem = try_join_all(elem.iter().map(|c| c.attr("href"))).await?;
    for i in elem{
        let link = format!("{}", i.unwrap());
        list.push(link);
    }
    Ok(list)
}

async fn next_page(driver: WebDriver, num: i8) -> Result<(), Box<dyn Error + Send + Sync>> {
    let next_page = driver.find(By::Css(&format!("a[aria-label='Page {}']", num))).await?;
    let next_page = next_page.attr("href").await?.unwrap();
    driver.goto::<&str>(next_page.as_ref()).await?;
    Ok(())
}