import {Flex} from "@chakra-ui/react";

export default function IconBox(props: { [x: string]: any; children: any; }) {
    const {variant, children, ...rest} = props;

    return (
        <Flex
            alignItems={"center"}
            justifyContent={"center"}
            borderRadius={"12px"}
            {...rest}
        >
            {children}
        </Flex>
    );
}
