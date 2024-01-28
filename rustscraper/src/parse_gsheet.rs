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

    for link in links {
        driver.goto::<&str>(link.as_ref()).await?;
        /*let elem_form = driver.find(By::Id("search-form")).await?;
        let elem_text = elem_form.find(By::Id("searchInput")).await?;
        elem_text.send_keys("selenium").await?;
        let elem_button = elem_form.find(By::Css("button[type='submit']")).await?;
        elem_button.click().await?;
        driver.query(By::ClassName("firstHeading")).first().await?;
        assert_eq!(driver.title().await?, "Selenium - Wikipedia");*/
        thread::sleep(Duration::new(1,0));
    }

    driver.quit().await?;

    Ok(())
    
}