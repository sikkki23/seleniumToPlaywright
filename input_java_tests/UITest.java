package com.example.tests;

import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class UITest {

    @Test
    public void testExampleDotComTitle() {
        WebDriver driver = new ChromeDriver();
        driver.get("https://example.com");

        String title = driver.getTitle();
        System.out.println("Page Title: " + title);
        assert title.contains("Example Domain");

        driver.quit();
    }
}
