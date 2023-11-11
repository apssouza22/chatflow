import {Button, IconButton, Menu, MenuButton, MenuItem, MenuList, Modal, ModalBody, ModalCloseButton, ModalContent, ModalHeader, ModalOverlay, Table, TableContainer, Tbody, Td, Th, Thead, Tr, useDisclosure} from "@chakra-ui/react";
import {DeleteIcon, EditIcon, HamburgerIcon, ViewIcon} from "@chakra-ui/icons";
import React, {useState} from "react";
import {ChatController} from "../../components/Chat";

interface DataTableProps {
    data: any;
    chatCtl: ChatController
    depth?: number;
}

function splitKey(data: any) {
    const list = Object.entries(data).map(([key, value]) => {
        if (!Array.isArray(value)) {
            return `${key}=${value}`
        }
    })
    return list.join("; ")
}

export function RenderDataTable({data, chatCtl}: DataTableProps) {
    const {
        isOpen,
        onOpen,
        onClose
    } = useDisclosure()
    const [modalContent, setModalContent] = useState<string>("")
    const isArray = Array.isArray(data);
    let tableNames = Object.keys(isArray ? data[0] : data);

    if (data == null) {
        return
    }

    function setPrompt(prompt: string) {
        chatCtl.setActionRequest({
            type: 'text',
            always: true,
            defaultValue: prompt
        })
    }

    function SmartRender(props: { item: any, index: string | number }) {
        let isString = typeof props.item === 'string';
        if (isString && (props.item.endsWith(".png") || props.item.endsWith(".jpg") || props.item.endsWith(".jpeg"))) {
            return (<img src={props.item as string}/>)
        }
        if (isString && props.item.startsWith("http")) {
            return (<a href={props.item} key={props.index}>{props.item as string}, </a>)
        }
        if (isString && props.item.length > 100) {
            let text = props.item as string;
            return (
                <span key={props.index}>
                    <ViewIcon cursor={"pointer"} onClick={() => {
                        setModalContent(text)
                        onOpen()
                    }}/>
                     {"  " + text.substring(0, 100)}...
                </span>
            )
        }
        return (<span key={props.index}>{props.item as string}</span>)
    }

    return (
        <>
            {/*{*/}
            {/*    isArray && data.length > 0 && <Button variant={"ghost"}*/}
            {/*                                          color={"blue.600"}*/}
            {/*                                          _hover={{color: "blue.400"}}*/}
            {/*                                          onClick={() => {*/}
            {/*                                              alert("Not implemented yet")*/}
            {/*                                          }} size="sm">View as a table</Button>*/}
            {/*}*/}

            {isArray && data.length == 0 && (<span>No data</span>)}

            <TableContainer bg={"white"}>
                <Table variant='simple'>
                    <Thead >
                        <Tr>
                            {tableNames.map((name) => (
                                <Th>{name}</Th>
                            ))}
                            {isArray && (<Th>Action</Th>)}
                        </Tr>
                    </Thead>
                    <Tbody>
                        {isArray && data.map((item, index) => (
                            <Tr>
                                {Object.values(item).map((value, index) => (
                                    <Td style={{"verticalAlign": "top"}}>
                                        <>
                                            {(
                                                typeof value === 'object' && value !== null ? (
                                                    <RenderDataTable data={value as any} chatCtl={chatCtl}/>
                                                ) : (
                                                    <SmartRender item={value} index={index}/>
                                                )
                                            )}
                                        </>
                                    </Td>
                                ))}
                                <Td style={{"verticalAlign": "top"}}>
                                    <Menu>
                                        <MenuButton
                                            as={IconButton}
                                            aria-label="Copy"
                                            icon={<HamburgerIcon/>}
                                            variant="primary"
                                            border={'1px solid #E2E8F0'}
                                            size="sm"
                                            mr={2}
                                            ml={2}
                                            mt={2}
                                        />
                                        <MenuList>
                                            <MenuItem icon={<EditIcon/>} onClick={() => {
                                                setPrompt(`Edit {{{RESOURCE_NAME_HERE}}} with the following: \`${splitKey(item)}\``)
                                            }}>
                                                Edit
                                            </MenuItem>
                                            <MenuItem icon={<DeleteIcon/>} onClick={() => {
                                                setPrompt(`Delete {{{RESOURCE_NAME_HERE}}} \`${splitKey(item)}\``)
                                            }}>
                                                Delete
                                            </MenuItem>
                                        </MenuList>
                                    </Menu>
                                </Td>
                            </Tr>
                        ))}
                        {!isArray && (
                            <Tr>
                                {Object.values(data).map((value, index) => (
                                    <Td style={{"verticalAlign": "top"}}>
                                        <>
                                            {(
                                                typeof value === 'object' && value !== null ? (
                                                    <RenderDataTable data={value as any} chatCtl={chatCtl}/>
                                                ) : (
                                                    <SmartRender item={value} index={index}/>
                                                )
                                            )}
                                        </>
                                    </Td>
                                ))}
                            </Tr>
                        )}
                    </Tbody>
                </Table>
            </TableContainer>
            <Modal isOpen={isOpen} onClose={onClose}>
                <ModalOverlay/>
                <ModalContent>
                    <ModalHeader>Field value</ModalHeader>
                    <ModalCloseButton/>
                    <ModalBody whiteSpace={"pre-wrap"}>
                        {modalContent}
                    </ModalBody>
                </ModalContent>
            </Modal>
        </>
    );
};




