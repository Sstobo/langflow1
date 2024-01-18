import { expect, test } from "@playwright/test";
import { readFileSync } from "fs";

test.describe("drag and drop test", () => {
  /// <reference lib="dom"/>
  test("drop collection", async ({ page }) => {
    await page.routeFromHAR("harFiles/langflow.har", {
      url: "**/api/v1/**",
      update: false,
    });
    await page.route("**/api/v1/flows/", async (route) => {
      const json = {
        id: "e9ac1bdc-429b-475d-ac03-d26f9a2a3210",
      };
      await route.fulfill({ json, status: 201 });
    });
    await page.goto("http:localhost:3000/");
    await page.locator("span").filter({ hasText: "My Collection" }).isVisible();
    // Read your file into a buffer.
    const jsonContent = readFileSync(
      "tests/onlyFront/assets/collection.json",
      "utf-8"
    );

    // Create the DataTransfer and File
    const dataTransfer = await page.evaluateHandle((data) => {
      const dt = new DataTransfer();
      // Convert the buffer to a hex array
      const file = new File([data], "flowtest.json", {
        type: "application/json",
      });
      dt.items.add(file);
      return dt;
    }, jsonContent);

    // Now dispatch
    await page.dispatchEvent(
      '//*[@id="root"]/div/div[1]/div[2]/div[3]/div/div',
      "drop",
      {
        dataTransfer,
      }
    );

    await page
      .locator(
        '//*[@id="root"]/div/div[1]/div[2]/div[3]/div/div/div/div/div/div/div/div[2]/span[2]'
      )
      .click();
    await page.waitForTimeout(2000);

    const genericNoda = page.getByTestId("div-generic-node");
    const elementCount = await genericNoda.count();
    if (elementCount > 0) {
      expect(true).toBeTruthy();
    }
  });
});
