use std::error::Error;
use thirtyfour::*;
use std::thread;
use std::time::Duration;
use rsautogui::{mouse, mouse::Button, mouse::ScrollAxis};

static TARGET: &str = "https://www.google.com/maps/search/salt+lake+city+restaurants/@40.6927001,-112.0451563,9z?entry=ttu";

#[tokio::main]
async fn main() ->  Result<(), Box<dyn Error + Send + Sync>> {

    let mut caps = DesiredCapabilities::firefox();
    caps.add_firefox_arg("--enable-automation")?;
    let driver = WebDriver::new("http://localhost:4444", caps).await?;

    driver.goto::<&str>(TARGET.as_ref()).await?;
    thread::sleep(Duration::new(5,0)); 
    mouse::click(Button::Left); 
    mouse::scroll(ScrollAxis::Y, 10);
    let mut n: i32 = 0;
    let mut list = Vec::new();
    //let mut elem = driver.find(By::ClassName("HlvSq")).await?;

    let elems = driver.find_all(By::XPath("/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div/div/a")).await?;
    for elem in elems{
        let property_value: String = elem.text().await?;
        list.push(property_value);
        n = n + 1;
    }

    println!("count: {}, return vals: {:?}", n, list);

    driver.quit().await?;

    Ok(())
    
}
