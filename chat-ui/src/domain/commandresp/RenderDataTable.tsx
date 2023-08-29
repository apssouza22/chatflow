import {Button, IconButton, Menu, MenuButton, MenuItem, MenuList, Modal, ModalBody, ModalCloseButton, ModalContent, ModalHeader, ModalOverlay, Table, TableContainer, Tbody, useDisclosure} from "@chakra-ui/react";
import {DeleteIcon, EditIcon, HamburgerIcon, ViewIcon} from "@chakra-ui/icons";
import {useState} from "react";
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
            {
                isArray && data.length > 0 && <Button variant={"ghost"}
                                                      color={"blue.600"}
                                                      _hover={{color: "blue.400"}}
                                                      onClick={() => {
                                                          alert("Not implemented yet")
                                                      }} size="sm">View as a table</Button>
            }

            {isArray && data.length == 0 && (<span>No data</span>)}

            <TableContainer bg={"white"}>
                <Table variant='simple' style={{borderBottom: "10px solid #edf2f7"}}>
                    <Tbody>
                        {Object.entries(data).map(([key, value]) => (
                            <tr key={key} style={{border: "1px solid #edf2f7"}}>
                                <td style={{"verticalAlign": "top", paddingRight: "5px"}}>
                                    {key}
                                </td>
                                <td>
                                    <>
                                        {(
                                            typeof value === 'object' && value !== null ? (
                                                <RenderDataTable data={value as any} chatCtl={chatCtl}/>
                                            ) : (
                                                <SmartRender item={value} index={key}/>
                                            )
                                        )}
                                    </>
                                </td>
                                {isArray && (
                                    <td style={{"verticalAlign": "top"}}>
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
                                                    setPrompt(`Edit {{{RESOURCE_NAME_HERE}}} with the following: \`${splitKey(value)}\``)
                                                }}>
                                                    Edit
                                                </MenuItem>
                                                <MenuItem icon={<DeleteIcon/>} onClick={() => {
                                                    setPrompt(`Delete {{{RESOURCE_NAME_HERE}}} ${key}. \`${splitKey(value)}\``)
                                                }}>
                                                    Delete
                                                </MenuItem>
                                            </MenuList>
                                        </Menu>
                                    </td>
                                )}
                            </tr>
                        ))}
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




