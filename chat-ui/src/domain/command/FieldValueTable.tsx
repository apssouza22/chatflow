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
    function flatFields(data:any): {} {
        const flatFields = {};
        const stack = [{obj: data, parentKey: null}];
        while (stack.length > 0) {
            const {obj, parentKey} = stack.pop();

            Object.keys(obj).forEach(key => {
                const val = obj[key];

                if (typeof val === "object") {
                    stack.push({obj: val, parentKey: parentKey ? `${parentKey}.${key}` : key});
                }

                if (typeof val === "string") {
                    flatFields[parentKey ? `${parentKey}.${key}` : key] = val;
                }
            });
        }
        return flatFields;
    }

    const onBlurHandler = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>): void => {
        const {
            name,
            value
        } = event.target
        // @ts-ignore
        setArgs(prevValues => {
            if (prevValues.hasOwnProperty(name)) {
                return {
                    ...prevValues!,
                    [name]: value
                }
            }
            let arr = {...prevValues}

            name
                .split(".")
                .forEach(key => {
                    if (arr.hasOwnProperty(key) && typeof arr[key] === "object") {
                        arr = arr[key]
                        return
                    }
                    arr[key] = value
                })

            return prevValues
        })
    }


    function handleValueField(key: string, fields): ReactJSXElement {
        if (!props.requestRender?.hasOwnProperty(key)) {
            return (<Input name={key} defaultValue={fields[key]} onBlur={onBlurHandler}/>)
        }
        if (props.requestRender[key]?.field_type == "password") {
            return (<Input type={"password"} name={key} defaultValue={fields[key]} onBlur={onBlurHandler}/>)
        }
        if (props.requestRender[key]?.field_type == "email") {
            return (<Input type={"email"} name={key} defaultValue={fields[key]} onBlur={onBlurHandler}/>)
        }
        if (props.requestRender[key]?.field_type == "checkbox") {
            return (<Input name={key} defaultValue={fields[key]} onBlur={onBlurHandler}/>)
        }
        if (props.requestRender[key]?.field_type == "textarea") {
            return (<Textarea name={key} defaultValue={fields[key]} onBlur={onBlurHandler}/>)
        }
        if (props.requestRender[key]?.field_type == "select") {
            return (<Select placeholder='Select option' name={key} defaultValue={fields[key]} onChange={onBlurHandler}>
                {props.requestRender[key]?.field_options?.map(v => (
                        <option value={v}>{v}</option>
                    )
                )}
            </Select>)
        }
        return (<Input name={key} defaultValue={fields[key]} onBlur={onBlurHandler}/>)
    }

    let fields = flatFields(args);
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
                        {Object.keys(fields).map(key => (
                            <Tr key={Math.random()}>
                                <Td>{key}</Td>
                                <Td>
                                    {handleValueField(key, fields)}
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
