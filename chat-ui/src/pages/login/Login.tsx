import {useState} from 'react';
import {Box, Heading, FormControl, FormLabel, Input, Button, Container, Center, VStack, Spinner, Link} from '@chakra-ui/react';
import {useRestAPI} from "../../hooks/useFetch";
import {NavLink, useNavigate} from "react-router-dom";
import {useChatContext} from "../../hooks/useChatContext";
import {SessionManager} from "../../domain/session/SessionManager";


export function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const {loading, post} = useRestAPI(process.env.REACT_APP_SERVER_URL)
    const {dispatch} = useChatContext()

    const navigate = useNavigate()

    const handleSubmit = async e => {
        e.preventDefault();
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
        const session = SessionManager.getInstance();
        // @ts-ignore
        let token = resp.data.access_token;
        session.setToken(token);
        session.setUser(email);
        sessionStorage.setItem("token", token)
        navigate("/chatflow")
    };

    return (
        <Container maxW="container.md" centerContent>
            <Center h="100vh">
                <VStack spacing={8}>
                    <Heading>Login</Heading>
                    <Box w="100%" p={4} borderWidth={1} borderRadius="lg">
                        <p>Login: admin@gmail.com - 123</p>
                        <form onSubmit={handleSubmit}>
                            <VStack spacing={4}>
                                <FormControl id="email" isRequired>
                                    <FormLabel>Email address</FormLabel>
                                    <Input
                                        name={"email"}
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
                                    Login
                                </Button>)}
                                <Link as={NavLink} to="/signup">Don't have an account? Sign up</Link>
                            </VStack>
                        </form>
                    </Box>
                </VStack>
            </Center>
        </Container>
    );
}

