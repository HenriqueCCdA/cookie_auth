import User from "../models/User.js";
import bcrypt from "bcryptjs";
import { generateAccessToken, generateRefreshToken } from "../auth/token.js";

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

  const accessToken = generateAccessToken({ id: user.id });
  const refreshToken = generateRefreshToken({ id: user.id });

  res
    .cookie("authAccessCookie", accessToken, {
      secure: false,
      httpOnly: true,
    })
    .cookie("authRefreshCookie", refreshToken, {
      secure: false,
      httpOnly: true,
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
      const accessToken = generateAccessToken({ id: newUser.id });
      const refreshToken = generateRefreshToken({ id: newUser.id });

      res
        .cookie("authAccessCookie", accessToken, {
          secure: false,
          httpOnly: true,
        })
        .cookie("authRefreshToken", refreshToken, {
          secure: false,
          httpOnly: true,
        });

      return res.status(201).json({
        id: newUser.id,
      });
    })
    .catch((err) => console.log(err));
};

const logout = (req, res) => {
  res.clearCookie("authAccessCookie");
  res.clearCookie("authRefreshCookie")
  return res.json({ auth: false });
};

const authController = { register, login, logout };
export default authController;
