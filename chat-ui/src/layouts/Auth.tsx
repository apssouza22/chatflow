import * as React from "react"
import {ChakraProvider,extendTheme} from "@chakra-ui/react"
import {Outlet} from "react-router-dom";
import customTheme from "../theme/customTheme";
const theme = extendTheme(customTheme)
/**
 * Layout to be used for all pages related to authentication. eg. Login, Register, Forgot Password, etc.
 */
export function Auth() {
    return (
        <ChakraProvider theme={theme}>
            <Outlet/>
        </ChakraProvider>
    );
}

