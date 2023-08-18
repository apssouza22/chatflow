import {Input, Select, Table, TableContainer, Tbody, Td, Textarea, Tfoot, Th, Thead, Tr} from "@chakra-ui/react"
import {useState} from "react";
import {BtnProceed} from "./BtnProceed";
import {Command, RequestRender} from "./Common";
import {ReactJSXElement} from "@emotion/react/types/jsx-namespace";
import {ChatController} from "../../components/Chat";

type FieldValueTableProps = {
    data: any
    chatCtl: ChatController
    command: Command
    requestRender?: Record<string, RequestRender>
};

export function FieldValueTable(props: FieldValueTableProps): JSX.Element {
    const [args, setArgs] = useState(props.data)
    if (props.data.length === 0) {
        return (<div>No data</div>)
    }
    const onBlurHandler = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>): void => {
        const {
            name,
            value
        } = event.target
        // @ts-ignore
        setArgs(prevValues => {
            return ({
                ...prevValues!,
                [name]: value
            })
        })
    }

    function handleValueField(key: string): ReactJSXElement {
        if (!props.requestRender?.hasOwnProperty(key)) {
            return (<Input name={key} defaultValue={args[key]} onBlur={onBlurHandler}/>)
        }
        if (props.requestRender[key]?.field_type == "password") {
            return (<Input type={"password"} name={key} defaultValue={args[key]} onBlur={onBlurHandler}/>)
        }
        if (props.requestRender[key]?.field_type == "email") {
            return (<Input type={"email"} name={key} defaultValue={args[key]} onBlur={onBlurHandler}/>)
        }
        if (props.requestRender[key]?.field_type == "checkbox") {
            return (<Input name={key} defaultValue={args[key]} onBlur={onBlurHandler}/>)
        }
        if (props.requestRender[key]?.field_type == "textarea") {
            return (<Textarea name={key} defaultValue={args[key]} onBlur={onBlurHandler}/>)
        }
        if (props.requestRender[key]?.field_type == "select") {
            return (<Select placeholder='Select option' name={key} defaultValue={args[key]} onChange={onBlurHandler}>
                {props.requestRender[key]?.field_options?.map(v => (
                        <option value={v}>{v}</option>
                    )
                )}
            </Select>)
        }
        return (<Input name={key} defaultValue={args[key]} onBlur={onBlurHandler}/>)
    }

    return (
        <>
            <TableContainer bg={"white"}>
                <Table variant='simple'>
                    <Thead>
                        <Tr>
                            <Th>Field</Th>
                            <Th>Value</Th>
                        </Tr>
                    </Thead>
                    <Tbody>
                        {Object.keys(args).map(key => (
                            <Tr key={Math.random()}>
                                <Td>{key}</Td>
                                <Td>
                                    {handleValueField(key)}
                                </Td>
                            </Tr>
                        ))}
                    </Tbody>
                    <Tfoot>
                        <Tr>
                            <Th>Field</Th>
                            <Th>Value</Th>
                        </Tr>
                    </Tfoot>
                </Table>
            </TableContainer>
            <BtnProceed command={props.command} commandData={args}  chatCtl={props.chatCtl}/>
        </>
    )
}
