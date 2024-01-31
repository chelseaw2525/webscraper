use std::error::Error;
use reqwest;
use scraper::{Html, Selector};
use thirtyfour::prelude::*;
use std::thread;
use std::time::Duration;

static TARGET: &str = "https://docs.google.com/spreadsheets/u/1/d/1TdjbZZjEVkCuqMCOCz0cEVC-lUTi9RNBx_YZOoN2N2U/htmlview";

#[tokio::main]
async fn main() ->  Result<(), Box<dyn Error + Send + Sync>> {
    let body = reqwest::get(TARGET).await?.text().await?;
    let document = Html::parse_document(&body);
    let selector = Selector::parse(r#"table > tbody > tr > td:nth-child(4)"#).unwrap();
    let mut links = Vec::new();
    for title in document.select(&selector) {
        let value = title.text();
        let link = value.collect::<String>();
        links.push(link);
    }

    let mut caps = DesiredCapabilities::chrome();
    caps.add_chrome_arg("--enable-automation")?;
    let driver = WebDriver::new("http://localhost:9515", caps).await?;

    for n in 44..203 {
        let link = &links[n];
        driver.goto::<&str>(link.as_ref()).await?;
        
        if !(link.contains("lu.ma")) {
            thread::sleep(Duration::new(10,0));   
        }
        //else {
            thread::sleep(Duration::new(15,0));
            /*
            let elem_button = driver.find(By::Css("button[type='button']")).await?.click().await?.unwrap();

            let name_field = driver.find(By::Id("rc")).await?.click().await?.expect("not found");
            name_field.send_keys(name).await?.except("not found");

            let email_field = driver.find(By::Id("rd")).await?.click().await?.expect("not found");
            email_field.send_keys(email).await?.except("not found");*/
        //}
    }

    driver.quit().await?;

    Ok(())
    
}