use std::error::Error;
//use csv;
use reqwest;
use scraper::{Node::Text, Html, Selector};



static TARGET: &str = "https://docs.google.com/spreadsheets/u/1/d/1TdjbZZjEVkCuqMCOCz0cEVC-lUTi9RNBx_YZOoN2N2U/htmlview";

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let body = reqwest::get(TARGET).await?.text().await?;
    let document = Html::parse_document(&body);
    let selector = Selector::parse(r#"table > tbody > tr > td: > a"#).unwrap();
    //let mut links = Vec::new();
    let mut itrs = 1;
    for title in document.select(&selector) {
        println!("row {}, {:?}", itrs, 
            title
                .value()
                .attr("href")
                .expect("href not found")
                .to_string()
        );
        itrs = itrs+1;
    }

    Ok(())
}