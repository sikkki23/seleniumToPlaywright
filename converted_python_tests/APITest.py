package com.example.tests;
import io.restassured.RestAssured;
import io.restassured.response.Response;
import org.junit.jupiter.api.Test;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.equalTo;
def test_apitest(page: Page):
@Test
public void testExampleAPI() {
Response response = RestAssured.get("https://jsonplaceholder.typicode.com/posts/1");
System.out.println("Response Body:\n" + response.getBody().asString());
assertThat(response.statusCode(), equalTo(200));
assertThat(response.jsonPath().getString("title"), equalTo("sunt aut facere repellat provident occaecati excepturi optio reprehenderit"));
}
}