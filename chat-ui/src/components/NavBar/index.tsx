import {Flex, Heading, Spacer, Image} from "@chakra-ui/react"

export default function Navbar() {

    return ( 
        <Flex as="nav" p="10px" alignItems="center" justifyContent="center" position={"fixed"} bg="#1B0462" width={"100%"} zIndex={1000}>
            <Image src="https://raw.githubusercontent.com/GiovanniSmokes/images/main/Untitled.png" alt="Logo" boxSize="30px" />
            <Spacer/>                     
        </Flex>
    )
}
