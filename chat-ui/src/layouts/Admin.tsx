import * as React from "react"
import {ChakraProvider, theme} from "@chakra-ui/react"
import {Outlet} from "react-router-dom";
import {RequiresAuth} from "../components/RequiresAuth";

/**
 * Layout to be used for all admin pages
 */
export function Admin() {
    return (
        <ChakraProvider theme={theme}>
            <RequiresAuth>
                <Outlet/>
            </RequiresAuth>
        </ChakraProvider>
    );
}

