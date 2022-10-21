import User from "../models/User.js";
import bcrypt from "bcryptjs";
import { generateToken } from "../auth/token.js";

const login = async (req, res) => {
  const { email, password } = req.body;

  const user = await User.findOne({ where: { email } });

  if (!user) {
    return res.status(401).json({ errors: ["Credenciais inválidas!"] });
  }

  const compairPasswords = bcrypt.compareSync(password, user.password);

  if (!compairPasswords) {
    return res.status(401).json({ errors: ["Credenciais inválidas!"] });
  }

  const jwtSecret = process.env.JWT_SECRET;
  const token = generateToken({ id: user.id }, jwtSecret);

  res.cookie("authCookie", token, {
    secure: false,
    httpOnly: true,
    // Almost 1 minute
    maxAge: 1 * 60 * 60 * 16.6,
  });

  return res.json({
    id: user.id,
  });
};

const register = async (req, res) => {
  const { name, email, password } = req.body;

  const checkIfUserExists = await User.findOne({ where: { email } });

  if (checkIfUserExists) {
    return res.status(409).json({ errors: ["O e-mail já está em uso."] });
  }

  const salt = bcrypt.genSaltSync(10);
  const hashedPassword = bcrypt.hashSync(password, salt);

  const user = { name, email, password: hashedPassword };

  User.create(user)
    .then((newUser) => {
      const jwtSecret = process.env.JWT_SECRET;
      const token = generateToken({ id: newUser.id }, jwtSecret);

      res.cookie("authCookie", token, {
        secure: false,
        httpOnly: true,
        // Almost 1 minute
        maxAge: 1 * 60 * 60 * 16.6,
      });

      return res.status(201).json({
        id: newUser.id,
      });
    })
    .catch((err) => console.log(err));
};

const logout = (req, res) => {
  res.clearCookie("authCookie");
  return res.json({ auth: false });
};

const getUserInfo = (req, res) => {
  const { user } = req;

  return res.json(user);
};

const userController = { login, register, logout, getUserInfo };

export default userController;
