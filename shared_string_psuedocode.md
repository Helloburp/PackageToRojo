# Title

## Notes

- There is only one SharedString per file.
- The shared string is always appended after the final item in the Roblox tag.
- The format is the following:

    ```xml
        <SharedStrings>
            <SharedString md5="yuZpQdnvvUBOTYh1jqZ2cA=="></SharedString>
        </SharedStrings>
    ```

    And, within the properties tag of the instance,

    ```xml
        <SharedString name="ModelMeshData">yuZpQdnvvUBOTYh1jqZ2cA==</SharedString>
    ```

1. Identify the string
