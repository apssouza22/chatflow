import {Box, Button, Center, Container, Flex, FormControl, FormLabel, Heading, Input, Link, Spinner, VStack} from '@chakra-ui/react';
import {useState} from 'react';
import {useRestAPI} from "../../hooks/useFetch";
import {useChatContext} from "../../hooks/useChatContext";
import {NavLink, useNavigate} from 'react-router-dom';
import {SessionManager} from "../../domain/session/SessionManager";

const SignupPage = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const {loading, post} = useRestAPI(process.env.REACT_APP_SERVER_URL)
    const {dispatch} = useChatContext()

    let navigate = useNavigate()

    const login = async () => {
        const resp = await post("/user/login", {
            "email": email,
            "password": password,
        })

        // @ts-ignore
        if (resp.status !== 200 || resp.data?.access_token == null) {
            alert("Login failed")
            return
        }
        dispatch({type: "LOGIN", payload: email})
        let session = SessionManager.getInstance();
        session.setToken(email);
        // @ts-ignore
        session.setToken(resp.data.access_token);
        navigate("/chatflow")
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (name == '' || email == '' || password == '') {
            alert("Please fill all fields")
        }

        const resp = await post("/user/register", {
            "email": email,
            "password": password,
            "name": name
        })

        if (resp.status !== 200) {
            alert("Signup failed")
            return
        }

        await login()
    };

    return (
        <Container maxW="container.md" centerContent>
            <Center h="100vh">
                <VStack spacing={8}>
                    <Heading>Sign Up</Heading>
                    <Box w="100%" p={4} borderWidth={1} borderRadius="lg">
                        <form onSubmit={handleSubmit}>
                            <VStack spacing={4}>
                                <FormControl id="name" isRequired>
                                    <FormLabel>Name</FormLabel>
                                    <Input
                                        type="name"
                                        placeholder="Enter your email"
                                        size="md"
                                        onChange={e => setName(e.target.value)}
                                    />
                                </FormControl>
                                <FormControl id="email" isRequired>
                                    <FormLabel>Email address</FormLabel>
                                    <Input
                                        type="email"
                                        placeholder="Enter your email"
                                        size="md"
                                        onChange={e => setEmail(e.target.value)}
                                    />
                                </FormControl>
                                <FormControl id="password" isRequired>
                                    <FormLabel>Password</FormLabel>
                                    <Input
                                        type="password"
                                        placeholder="Enter your password"
                                        size="md"
                                        onChange={e => setPassword(e.target.value)}
                                    />
                                </FormControl>
                                {loading && <Spinner/>}
                                {!loading && (<Button colorScheme="blue" type="submit" mt={4}>
                                    Sign Up
                                </Button>)}
                                <Link as={NavLink} to="/login">Already have an account? Log in</Link>
                            </VStack>
                        </form>
                    </Box>
                </VStack>
            </Center>
        </Container>
    );
};

export default SignupPage;
